import os
import torch
from torch.utils.data import Dataset
import rasterio
import numpy as np

class ISRODataset(Dataset):
    def __init__(self, image_dir, mask_dir, transforms=None):
        """
        Args:
            image_dir (str): Directory containing 4-band GeoTIFF images.
            mask_dir (str): Directory containing segmentation masks.
            transforms (callable, optional): Optional transform to be applied on a sample.
        """
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.image_files = sorted(os.listdir(image_dir))
        self.mask_files = sorted(os.listdir(mask_dir))
        self.transforms = transforms

    def __len__(self):
        return len(self.image_files)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_files[idx])
        mask_path = os.path.join(self.mask_dir, self.mask_files[idx])
        
        try:
            # Read 4-channel image (R, G, B, SWIR)
            with rasterio.open(img_path) as src:
                if src.count < 4:
                    raise ValueError(f"Image {img_path} has fewer than 4 bands (found {src.count}).")
                # Assuming bands 1,2,3 are RGB and 4 is SWIR
                image = src.read([1, 2, 3, 4]) 
                # Normalize to 0-1
                image = image.astype(np.float32) / 255.0 
                image = torch.from_numpy(image)

            # Read mask
            with rasterio.open(mask_path) as src:
                mask = src.read(1) # Assuming single band mask with class indices (0-3)
                mask = torch.from_numpy(mask).long()
                
            if self.transforms:
                # Note: Custom transforms for multiband imagery and masks should be handled here
                pass
                
            return image, mask
            
        except (rasterio.errors.RasterioIOError, FileNotFoundError) as e:
            raise RuntimeError(f"Failed to load image or mask at index {idx}. Is the file path correct? Error: {e}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error processing data at index {idx}: {e}")
