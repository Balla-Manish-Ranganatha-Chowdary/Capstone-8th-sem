import io
import torch
import numpy as np
import rasterio
from PIL import Image
from transformers import AutoModel
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Global model variables
_model = None
model_loaded = False

DEVICE = torch.device("cpu")
MODEL_NAME = os.getenv("MODEL_NAME", "ibm-nasa-geospatial/Prithvi-EO-1.0-100M")

def load_model():
    global _model, model_loaded
    try:
        logger.info(f"Loading model {MODEL_NAME} on {DEVICE}...")
        _model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)
        _model.eval()
        for param in _model.parameters():
            param.requires_grad = False
        _model.to(DEVICE)
        model_loaded = True
        logger.info("Model loaded and frozen successfully.")
    except Exception as e:
        model_loaded = False
        logger.error(f"Failed to load model: {e}")

def get_model_status():
    return model_loaded, MODEL_NAME, str(DEVICE)

def preprocess_image(file_bytes: bytes, filename: str) -> tuple[torch.Tensor, np.ndarray]:
    """
    Returns:
      tensor_img: torch.FloatTensor of shape [1, 6, 224, 224] for Prithvi
      raw_norm_img: np.ndarray of shape [6, 224, 224] for Stage 3 analysis
    """
    try:
        if filename.lower().endswith(('.tif', '.tiff')):
            with rasterio.MemoryFile(file_bytes) as memfile:
                with memfile.open() as dataset:
                    img_array = dataset.read() # Shape: [bands, H, W]
        else:
            img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
            img_array = np.array(img).transpose((2, 0, 1)).astype(np.float32) # Shape: [3, H, W]
            
        bands, h, w = img_array.shape
        
        # If 3 bands, pad with zero 4th band (SWIR)
        if bands == 3:
            swir_band = np.zeros((1, h, w), dtype=img_array.dtype)
            img_array = np.concatenate([img_array, swir_band], axis=0)
            bands = 4
            
        # Normalize each band to [0.0, 1.0]
        norm_array = np.zeros_like(img_array, dtype=np.float32)
        for i in range(bands):
            b_min, b_max = img_array[i].min(), img_array[i].max()
            if b_max > b_min:
                norm_array[i] = (img_array[i] - b_min) / (b_max - b_min)
            else:
                norm_array[i] = 0.0
                
        # Resize to 224x224 using torch.nn.functional.interpolate
        norm_tensor = torch.from_numpy(norm_array).unsqueeze(0) # [1, bands, H, W]
        resized_tensor = torch.nn.functional.interpolate(
            norm_tensor, size=(224, 224), mode='bilinear', align_corners=False
        ) # [1, bands, 224, 224]
        
        resized_array = resized_tensor.squeeze(0).numpy() # [bands, 224, 224]
        
        # Prithvi expects 6 bands, pad with zeros for bands 5 and 6
        final_array = np.zeros((6, 224, 224), dtype=np.float32)
        copy_bands = min(bands, 6)
        final_array[:copy_bands, :, :] = resized_array[:copy_bands, :, :]
        
        # Prepare for model
        tensor_img = torch.from_numpy(final_array).unsqueeze(0) # [1, 6, 224, 224]
        tensor_img = tensor_img.to(DEVICE)
        
        return tensor_img, final_array
    except Exception as e:
        logger.error(f"Preprocessing failed for {filename}: {str(e)}")
        raise e

@torch.no_grad()
def extract_features(tensor_img: torch.Tensor) -> np.ndarray:
    if not model_loaded or _model is None:
        raise RuntimeError("Model is not loaded.")
        
    outputs = _model(tensor_img)
    last_hidden_state = outputs.last_hidden_state # [1, num_patches, embedding_dim]
    feature_map = last_hidden_state.squeeze(0).cpu().numpy() # [num_patches, embedding_dim]
    return feature_map
