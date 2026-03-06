import os
import json
import logging
import torch
import torch.nn.functional as F
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import rasterio
from typing import Dict, Any, List, Tuple
from tqdm import tqdm

from CNN.model import build_model, load_pretrained
from CNN.dataset import ISROSatelliteDataset, InferenceLoader

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
CLASS_NAMES = {
    0: "background",
    1: "vegetation",
    2: "dense_forest",
    3: "water_bodies",
    4: "built_up_area",
    5: "barren_soil",
    6: "flooded_area",
    7: "snow_glacial"
}

COLOR_PALETTE = {
    0: (0, 0, 0),        # black
    1: (50, 205, 50),    # lime green
    2: (0, 100, 0),      # dark green
    3: (0, 0, 255),      # blue
    4: (255, 0, 0),      # red
    5: (210, 180, 140),  # tan
    6: (0, 255, 255),    # cyan
    7: (255, 255, 255)   # white
}

def get_class_name(idx: int) -> str:
    return CLASS_NAMES.get(idx, f"class_{idx}")

def load_and_preprocess(state_name: str, year: int, image_dir: str) -> torch.Tensor:
    """Uses InferenceLoader to load multi-band satellite image as a standard normalized tensor."""
    logging.info(f"Loading image for {state_name} - {year}")
    return InferenceLoader.load_state_image(state_name, year, image_dir)

def run_segmentation(model: torch.nn.Module, image_tensor: torch.Tensor, device: str = 'cuda', tile_size=512, overlap=64) -> Tuple[torch.Tensor, Dict[str, float]]:
    """Runs tiled inference with Gaussian blending to reconstruct the full resolution map."""
    model.eval()
    model.to(device)
    
    c, h, w = image_tensor.shape
    stride = tile_size - overlap
    
    num_classes = model.num_classes if hasattr(model, 'num_classes') else 8
    
    full_probs = torch.zeros((num_classes, h, w), device=device, dtype=torch.float32)
    weight_map = torch.zeros((1, h, w), device=device, dtype=torch.float32)
    
    # Pre-compute Gaussian kernel
    y = torch.linspace(-1, 1, tile_size)
    x = torch.linspace(-1, 1, tile_size)
    yy, xx = torch.meshgrid(y, x, indexing='ij')
    gaussian_kernel = torch.exp(-(xx**2 + yy**2) / (2 * (0.5**2))).to(device).unsqueeze(0)
    
    logging.info("Running tile-based segmentation...")
    with torch.no_grad():
        for r in tqdm(range(0, h, stride), desc="Rows"):
            for c_idx in range(0, w, stride):
                r_end = min(r + tile_size, h)
                c_end = min(c_idx + tile_size, w)
                
                r_start = max(0, r_end - tile_size)
                c_start = max(0, c_end - tile_size)
                
                tile = image_tensor[:, r_start:r_end, c_start:c_end]
                # Pad if requested edge tiles are smaller than tile_size (rare if starts logic holds, but standard safeguard)
                if tile.shape[1] < tile_size or tile.shape[2] < tile_size:
                    tile = F.pad(tile, (0, tile_size - tile.shape[2], 0, tile_size - tile.shape[1]))
                
                tile = tile.unsqueeze(0).to(device)
                logits = model(tile)
                probs = F.softmax(logits, dim=1)[0]
                
                full_probs[:, r_start:r_end, c_start:c_end] += probs * gaussian_kernel
                weight_map[:, r_start:r_end, c_start:c_end] += gaussian_kernel

    weight_map[weight_map == 0] = 1e-6
    full_probs /= weight_map
    
    max_probs, class_map = torch.max(full_probs, dim=0)
    
    # Valid coverage implies it is non-background 
    valid_mask = class_map > 0
    valid_ratio = valid_mask.float().mean().item()
    if valid_ratio < 0.3:
        raise ValueError(f"Insufficient valid coverage: {valid_ratio * 100:.2f}%")
        
    mean_conf = max_probs[valid_mask].mean().item() if valid_ratio > 0 else 0.0
    low_conf_area = (max_probs[valid_mask] < 0.6).float().mean().item() * 100 if valid_ratio > 0 else 0.0
    
    conf_dict = {
        "mean_confidence": mean_conf,
        "low_confidence_area_percentage": low_conf_area
    }
    
    return class_map.cpu(), conf_dict

def compute_class_statistics(mask: torch.Tensor, resolution_meters: float = 30.0) -> Dict[str, Dict[str, float]]:
    """Counts pixels per class and computes physical area."""
    counts = torch.bincount(mask.flatten(), minlength=8)
    pixel_area_km2 = (resolution_meters ** 2) / 1e6
    
    valid_pixels = counts[1:].sum().item()
    stats = {}
    
    for cls_idx in range(8):
        count = counts[cls_idx].item()
        area_km2 = count * pixel_area_km2
        
        # Percentage ignores background 
        pct = (count / valid_pixels * 100) if valid_pixels > 0 and cls_idx > 0 else 0.0
        
        stats[get_class_name(cls_idx)] = {
            "pixel_count": count,
            "area_km2": float(area_km2),
            "percentage": float(pct)
        }
    return stats

def compute_change_matrix(mask_t1: torch.Tensor, mask_t2: torch.Tensor, num_classes: int = 8) -> np.ndarray:
    """Computes transition matrix from class i to class j."""
    m1, m2 = mask_t1.flatten(), mask_t2.flatten()
    idx = m1 * num_classes + m2
    counts = torch.bincount(idx, minlength=num_classes**2)
    return counts.view(num_classes, num_classes).numpy()

def compute_percentage_changes(
    stats_t1: dict, 
    stats_t2: dict, 
    change_matrix: np.ndarray, 
    state: str, 
    start_year: int, 
    end_year: int,
    conf_dict: dict,
    resolution_meters: float = 30.0
) -> dict:
    """Combines metrics to output the final standardized JSON contract dictionary."""
    num_classes = 8
    pixel_area_km2 = (resolution_meters ** 2) / 1e6
    
    total_valid_area_km2 = sum(stats_t2[get_class_name(i)]['area_km2'] for i in range(1, num_classes))
    
    class_changes = {}
    for i in range(1, num_classes):
        cls_name = get_class_name(i)
        
        a1, a2 = stats_t1[cls_name]['area_km2'], stats_t2[cls_name]['area_km2']
        p1, p2 = stats_t1[cls_name]['percentage'], stats_t2[cls_name]['percentage']
        
        abs_change = a2 - a1
        pct_change = (abs_change / a1 * 100) if a1 > 0 else (100.0 if a2 > 0 else 0.0)
        
        class_changes[cls_name] = {
            "area_km2_t1": a1,
            "area_km2_t2": a2,
            "percentage_t1": p1,
            "percentage_t2": p2,
            "absolute_change_km2": abs_change,
            "percentage_change": pct_change,
            "confidence": conf_dict.get('mean_confidence', 0.0)
        }
        
    top_transitions = []
    # Ignore background transitions
    valid_transitions = change_matrix[1:, 1:].sum() * pixel_area_km2
    
    for i in range(1, num_classes):
        for j in range(1, num_classes):
            if i == j or change_matrix[i, j] == 0:
                continue
            
            t_area = change_matrix[i, j] * pixel_area_km2
            t_pct = (t_area / valid_transitions * 100) if valid_transitions > 0 else 0.0
            
            top_transitions.append({
                "from_class": get_class_name(i),
                "to_class": get_class_name(j),
                "area_km2": float(t_area),
                "percentage_of_total": float(t_pct)
            })
            
    top_transitions = sorted(top_transitions, key=lambda x: x['area_km2'], reverse=True)[:10]
    
    return {
        "state": state,
        "start_year": start_year,
        "end_year": end_year,
        "resolution_meters": resolution_meters,
        "total_valid_area_km2": float(total_valid_area_km2),
        "class_changes": class_changes,
        "top_transitions": top_transitions,
        "segmentation_confidence": conf_dict
    }

def visualize_segmentation(mask: np.ndarray, title: str, save_path: str):
    """Visualizes standard class map and saves to path."""
    rgb = np.zeros((*mask.shape, 3), dtype=np.uint8)
    for c_idx, color in COLOR_PALETTE.items():
        rgb[mask == c_idx] = color
        
    plt.figure(figsize=(10, 10))
    plt.imshow(rgb)
    plt.title(title)
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def visualize_change_map(mask_t1: torch.Tensor, mask_t2: torch.Tensor, save_path: str):
    """Highlights modified pixels by color of destination class, greyscale for unchanged."""
    m1 = mask_t1.numpy()
    m2 = mask_t2.numpy()
    
    changed = m1 != m2
    
    rgb = np.zeros((*m1.shape, 3), dtype=np.uint8)
    rgb[~changed] = (128, 128, 128)  # Grey for unchanged
    
    for c_idx, color in COLOR_PALETTE.items():
        if c_idx > 0:
            mask_current_class_change = changed & (m2 == c_idx)
            rgb[mask_current_class_change] = color
            
    plt.figure(figsize=(10, 10))
    plt.imshow(rgb)
    plt.title("Change Map (Colored by New Class)")
    plt.axis('off')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_change_barchart(change_dict: dict, save_path: str):
    """Plots a barchart of absolute change per class."""
    classes = []
    changes = []
    for cls_name, vals in change_dict['class_changes'].items():
        classes.append(cls_name)
        changes.append(vals['absolute_change_km2'])
        
    plt.figure(figsize=(12, 6))
    plt.bar(classes, changes, color=['red' if x < 0 else 'green' for x in changes])
    plt.axhline(0, color='black', linewidth=1)
    plt.xticks(rotation=45, ha='right')
    plt.ylabel('Change in Area (km²)')
    plt.title(f"Land Cover Change: {change_dict['state']} ({change_dict['start_year']} to {change_dict['end_year']})")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def detect_changes(
    state_name: str,
    start_year: int,
    end_year: int,
    image_dir: str,
    model_checkpoint: str,
    device: str = 'cuda'
) -> dict:
    """End-to-end inference and change detection system."""
    logging.info(f"Starting change detection for {state_name} ({start_year} -> {end_year})")
    
    # Init Model
    model = build_model({'backbone': 'resnet50', 'num_classes': 8, 'pretrained': False})
    model = load_pretrained(model, model_checkpoint)
    
    # 1. Load Data
    img_t1 = load_and_preprocess(state_name, start_year, image_dir)
    img_t2 = load_and_preprocess(state_name, end_year, image_dir)
    
    # 2. Run Segmentation
    mask_t1, conf_t1 = run_segmentation(model, img_t1, device)
    mask_t2, conf_t2 = run_segmentation(model, img_t2, device)
    
    # Compile joint confidence
    joint_conf = {
        "mean_confidence": (conf_t1['mean_confidence'] + conf_t2['mean_confidence']) / 2.0,
        "low_confidence_area_percentage": max(conf_t1['low_confidence_area_percentage'], conf_t2['low_confidence_area_percentage'])
    }
    
    # 3. Class Stats
    stats_t1 = compute_class_statistics(mask_t1)
    stats_t2 = compute_class_statistics(mask_t2)
    
    # 4. Change Matrix
    change_matrix = compute_change_matrix(mask_t1, mask_t2)
    
    # 5. Percentage Changes and Output Contract Dict
    final_dict = compute_percentage_changes(
        stats_t1, stats_t2, change_matrix, 
        state_name, start_year, end_year, 
        conf_dict=joint_conf
    )
    
    logging.info("Change detection successfully generated.")
    return final_dict

def batch_detect_changes(state_list: list, start_year: int, end_year: int, image_dir: str, model_checkpoint: str, output_dir: str, device: str = 'cuda') -> list:
    """Processes multiple states and caches results to JSON safely."""
    results = []
    os.makedirs(output_dir, exist_ok=True)
    
    for state in state_list:
        cache_path = os.path.join(output_dir, f"{state}_{start_year}_{end_year}.json")
        if os.path.exists(cache_path):
            logging.info(f"Using cached result for {state}")
            with open(cache_path, 'r') as f:
                results.append(json.load(f))
            continue
            
        try:
            result = detect_changes(state, start_year, end_year, image_dir, model_checkpoint, device)
            results.append(result)
            
            with open(cache_path, 'w') as f:
                json.dump(result, f, indent=2)
        except Exception as e:
            logging.error(f"Failed processing {state}: {str(e)}")
            
    return results
