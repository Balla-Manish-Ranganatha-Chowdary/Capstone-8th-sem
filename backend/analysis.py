import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

def run_change_analysis(
    feature_map_t1: np.ndarray, 
    feature_map_t2: np.ndarray,
    img_t1: np.ndarray, 
    img_t2: np.ndarray
) -> dict:
    
    num_patches = feature_map_t1.shape[0]
    
    # PART A: Embedding Map
    delta = feature_map_t2 - feature_map_t1
    magnitude = np.linalg.norm(delta, axis=1)
    
    mag_min = magnitude.min()
    mag_max = magnitude.max()
    magnitude_norm = (magnitude - mag_min) / (mag_max - mag_min + 1e-8)
    
    sim = cosine_similarity(feature_map_t1, feature_map_t2)
    patch_similarity = np.diag(sim)
    
    changed_mask = patch_similarity < 0.85
    changed_ratio = np.sum(changed_mask) / num_patches
    changed_area_percent = float(changed_ratio * 100.0)
    
    change_magnitude_mean = float(np.mean(magnitude_norm))
    change_magnitude_max = float(np.max(magnitude_norm))
    
    # PART B: Raw Image Bands
    # 0=Red, 1=Green, 2=Blue, 3=SWIR
    
    # NDVI proxy (img_t[1] - img_t[0]) / (img_t[1] + img_t[0] + 1e-8)
    ndvi_t1 = (img_t1[1] - img_t1[0]) / (img_t1[1] + img_t1[0] + 1e-8)
    ndvi_t2 = (img_t2[1] - img_t2[0]) / (img_t2[1] + img_t2[0] + 1e-8)
    
    ndvi_mean_t1 = float(np.mean(ndvi_t1))
    ndvi_mean_t2 = float(np.mean(ndvi_t2))
    
    vegetation_change_percent = ((ndvi_mean_t2 - ndvi_mean_t1) / (abs(ndvi_mean_t1) + 1e-8)) * 100.0
    
    # NDWI proxy (img_t[1] - img_t[3]) / (img_t[1] + img_t[3] + 1e-8)
    ndwi_t1 = (img_t1[1] - img_t1[3]) / (img_t1[1] + img_t1[3] + 1e-8)
    ndwi_t2 = (img_t2[1] - img_t2[3]) / (img_t2[1] + img_t2[3] + 1e-8)
    
    ndwi_mean_t1 = float(np.mean(ndwi_t1))
    ndwi_mean_t2 = float(np.mean(ndwi_t2))
    
    water_body_change_percent = ((ndwi_mean_t2 - ndwi_mean_t1) / (abs(ndwi_mean_t1) + 1e-8)) * 100.0
    
    # Bare soil
    soil_mask_t1 = (ndvi_t1 < 0.2) & (ndwi_t1 < 0.0)
    soil_mask_t2 = (ndvi_t2 < 0.2) & (ndwi_t2 < 0.0)
    
    bare_soil_t1 = float(np.mean(soil_mask_t1)) * 100.0
    bare_soil_t2 = float(np.mean(soil_mask_t2)) * 100.0
    bare_soil_exposure_percent = bare_soil_t2 - bare_soil_t1
    
    # PART C: Dominant Change
    if water_body_change_percent > 15:
        dominant_change_type = "water_expansion"
    elif water_body_change_percent < -15:
        dominant_change_type = "water_recession"
    elif vegetation_change_percent < -20:
        dominant_change_type = "vegetation_loss"
    elif vegetation_change_percent > 20:
        dominant_change_type = "vegetation_gain"
    elif bare_soil_exposure_percent > 15:
        dominant_change_type = "soil_exposure"
    elif changed_area_percent > 30:
        dominant_change_type = "urban_spread"
    else:
        dominant_change_type = "mixed"
        
    # PART D: Risk Level classification
    if changed_area_percent < 10:
        risk_level = "low"
    elif changed_area_percent < 25:
        risk_level = "moderate"
    elif changed_area_percent < 50:
        risk_level = "high"
    else:
        risk_level = "critical"
        
    return {
        "changed_area_percent": float(changed_area_percent),
        "vegetation_change_percent": float(vegetation_change_percent),
        "water_body_change_percent": float(water_body_change_percent),
        "bare_soil_exposure_percent": float(bare_soil_exposure_percent),
        "change_magnitude_mean": float(change_magnitude_mean),
        "change_magnitude_max": float(change_magnitude_max),
        "dominant_change_type": dominant_change_type,
        "risk_level": risk_level
    }
