import os
import glob
import torch
from torch.utils.data import Dataset
import numpy as np
import rasterio
from rasterio.windows import Window
import albumentations as A
import logging
from typing import Optional, Tuple, Dict, Any, List
import math

class ISROSatelliteDataset(Dataset):
    """
    Dataset to load paired ISRO satellite imagery tiles.
    Bands: [R, G, B, SWIR1, SWIR2]
    """
    
    # ISRO Resourcesat-2 approximate values
    BAND_MEANS = [0.485, 0.456, 0.406, 0.350, 0.310]
    BAND_STDS  = [0.229, 0.224, 0.225, 0.180, 0.160]

    def __init__(
        self, 
        image_dir: str, 
        mask_dir: str, 
        split: str = 'train', 
        tile_size: int = 512, 
        overlap: int = 64, 
        transform: Optional[A.Compose] = None
    ):
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.split = split
        self.tile_size = tile_size
        self.overlap = overlap
        self.stride = self.tile_size - self.overlap
        self.transform = transform
        
        if split == 'train' and not self.transform:
            self.transform = self._get_default_train_transform()
            
        self.tiles = self._generate_tile_indices()

    def _get_default_train_transform(self):
        # We split image into RGB and SWIR internally in __getitem__ to apply brightness
        return A.Compose([
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.5),
            A.RandomRotate90(p=0.5),
            A.GridDistortion(p=0.2),
            A.CoarseDropout(max_holes=8, max_height=32, max_width=32, p=0.2)
        ], additional_targets={'swir': 'image'})

    def _apply_rgb_brightness_contrast(self, img: np.ndarray, p: float = 0.3) -> np.ndarray:
        if np.random.rand() < p:
            alpha = 1.0 + np.random.uniform(-0.2, 0.2)
            beta = np.random.uniform(-0.1, 0.1)
            # img is already normalized, so this is an approximation of brightness/contrast
            img[..., :3] = img[..., :3] * alpha + beta
        return img

    def _generate_tile_indices(self) -> List[Tuple[str, str, int, int]]:
        tiles = []
        image_files = glob.glob(os.path.join(self.image_dir, '*.tif'))
        
        for img_path in image_files:
            basename = os.path.basename(img_path)
            # Find matching mask: if img is andhra_pradesh_2019.tif, mask might be andhra_pradesh_2019_mask.tif
            mask_name = basename.replace('.tif', '_mask.tif')
            mask_path = os.path.join(self.mask_dir, mask_name)
            
            if not os.path.exists(mask_path):
                # Try .png
                mask_name = basename.replace('.tif', '_mask.png')
                mask_path = os.path.join(self.mask_dir, mask_name)
                
            if not os.path.exists(mask_path):
                logging.warning(f"No mask found for {img_path}, skipping.")
                continue
                
            with rasterio.open(img_path) as src:
                h, w = src.height, src.width
                
            for r in range(0, h - self.tile_size + 1, self.stride):
                for c in range(0, w - self.tile_size + 1, self.stride):
                    tiles.append((img_path, mask_path, r, c))
                    
        return tiles

    def __len__(self) -> int:
        return len(self.tiles)

    def __getitem__(self, idx: int) -> dict:
        img_path, mask_path, r, c = self.tiles[idx]
        
        window = Window(c, r, self.tile_size, self.tile_size)
        
        with rasterio.open(img_path) as src:
            # 1=R, 2=G, 3=B, 4=SWIR1, 5=SWIR2
            img_bands = src.read([1, 2, 3, 4, 5], window=window)
            img_nodata = src.nodata
            meta = src.meta
            
        with rasterio.open(mask_path) as src:
            mask = src.read(1, window=window)
            
        img = np.transpose(img_bands, (1, 2, 0)).astype(np.float32)
        
        if img_nodata is not None:
            validity_mask = np.any(img != img_nodata, axis=-1)
            img[img == img_nodata] = 0
        else:
            validity_mask = np.any(img > 0, axis=-1)
            
        for i in range(5):
            img[..., i] = (img[..., i] - self.BAND_MEANS[i]) / self.BAND_STDS[i]
            
        if self.split == 'train':
            img = self._apply_rgb_brightness_contrast(img, p=0.3)
            
        if self.transform is not None:
            rgb = img[..., :3]
            swir = img[..., 3:]
            augmented = self.transform(image=rgb, mask=mask, swir=swir)
            img = np.concatenate([augmented['image'], augmented['swir']], axis=-1)
            mask = augmented['mask']
            
        # Convert to tensors
        img_tensor = torch.from_numpy(img).permute(2, 0, 1).float()
        mask_tensor = torch.from_numpy(mask).long()
        validity_tensor = torch.from_numpy(validity_mask).bool()

        # Parse state and year from filename
        basename = os.path.basename(img_path)
        parts = basename.replace('.tif', '').split('_')
        year = int(parts[-1]) if parts[-1].isdigit() else 0
        state = "_".join(parts[:-1]) if parts[-1].isdigit() else basename
        
        return {
            'image': img_tensor,
            'mask': mask_tensor,
            'validity_mask': validity_tensor,
            'metadata': {
                'state': state,
                'year': year,
                'tile_row': r,
                'tile_col': c,
                'original_shape': (meta['height'], meta['width'])
            }
        }

class InferenceLoader:
    @staticmethod
    def load_state_image(state_name: str, year: int, image_dir: str) -> torch.Tensor:
        """
        Loads the full state image for a given year.
        Assumes normalized output.
        """
        pattern = os.path.join(image_dir, f"{state_name}_{year}*.tif")
        matches = glob.glob(pattern)
        if not matches:
            raise FileNotFoundError(f"Image not found for {state_name} {year} in {image_dir}")
            
        img_path = matches[0]
        with rasterio.open(img_path) as src:
            img_bands = src.read([1, 2, 3, 4, 5])
            img_nodata = src.nodata
            
        img = np.transpose(img_bands, (1, 2, 0)).astype(np.float32)
        if img_nodata is not None:
            img[img == img_nodata] = 0
            
        for i in range(5):
            img[..., i] = (img[..., i] - ISROSatelliteDataset.BAND_MEANS[i]) / ISROSatelliteDataset.BAND_STDS[i]
            
        return torch.from_numpy(img).permute(2, 0, 1).float()

    @staticmethod
    def generate_tiles(image_tensor: torch.Tensor, tile_size: int = 512, overlap: int = 64) -> Tuple[List[torch.Tensor], List[Tuple[int, int]]]:
        """
        Generates tiles from a full image tensor.
        """
        _, h, w = image_tensor.shape
        stride = tile_size - overlap
        
        tiles = []
        coords = []
        
        for r in range(0, h, stride):
            for c in range(0, w, stride):
                r_end = min(r + tile_size, h)
                c_end = min(c + tile_size, w)
                
                # Adjust r, c if tile goes out of bounds to always get tile_size x tile_size
                r_start = max(0, r_end - tile_size)
                c_start = max(0, c_end - tile_size)
                
                tile = image_tensor[:, r_start:r_end, c_start:c_end]
                tiles.append(tile)
                coords.append((r_start, c_start))
                
        return tiles, coords

    @staticmethod
    def reconstruct_from_tiles(
        tiles: list[torch.Tensor], 
        coords: list[Tuple[int, int]], 
        original_shape: tuple, 
        tile_size: int = 512
    ) -> torch.Tensor:
        """
        Reconstructs the full image mask from predicted tiles using Gaussian blending.
        """
        h, w = original_shape
        num_classes = tiles[0].shape[0] # Assumes tiles are (C, H, W) logits/probs
        
        full_map = torch.zeros((num_classes, h, w), device=tiles[0].device, dtype=torch.float32)
        weight_map = torch.zeros((1, h, w), device=tiles[0].device, dtype=torch.float32)
        
        # Create 2D Gaussian kernel
        y = torch.linspace(-1, 1, tile_size)
        x = torch.linspace(-1, 1, tile_size)
        yy, xx = torch.meshgrid(y, x, indexing='ij')
        gaussian_kernel = torch.exp(-(xx**2 + yy**2) / (2 * 0.5**2))
        gaussian_kernel = gaussian_kernel.to(tiles[0].device).unsqueeze(0) # (1, H, W)
        
        for tile, (r, c) in zip(tiles, coords):
            full_map[:, r:r+tile_size, c:c+tile_size] += tile * gaussian_kernel
            weight_map[:, r:r+tile_size, c:c+tile_size] += gaussian_kernel
            
        weight_map[weight_map == 0] = 1e-6
        full_map = full_map / weight_map
        
        # Return argmax
        return torch.argmax(full_map, dim=0)
