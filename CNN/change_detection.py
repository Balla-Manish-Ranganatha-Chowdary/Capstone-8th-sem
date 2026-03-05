import rasterio
import numpy as np

# Class mappings based on requirement
CLASSES = {
    0: "Barren Land",
    1: "Buildings",
    2: "Water Bodies",
    3: "Vegetation"
}

def calculate_area_from_mask(mask, pixel_area_sqm):
    """
    Calculates the area in square kilometers for each class in the mask.
    """
    areas = {}
    for class_id, class_name in CLASSES.items():
        pixel_count = np.sum(mask == class_id)
        area_sqkm = (pixel_count * pixel_area_sqm) / 1e6
        areas[class_name] = area_sqkm
    return areas

def detect_changes(mask_year_a_path, mask_year_b_path):
    """
    Compares two classification masks and calculates percentage changes.
    """
    try:
        with rasterio.open(mask_year_a_path) as src_a, rasterio.open(mask_year_b_path) as src_b:
            mask_a = src_a.read(1)
            mask_b = src_b.read(1)
            
            if mask_a.shape != mask_b.shape:
                raise ValueError(f"Mask shapes do not match: Year A is {mask_a.shape}, Year B is {mask_b.shape}. " 
                                 "Images must cover the same area.")
            
            # Calculate pixel area (assuming CRS is projected and units are meters)
            # transform[0] is pixel width, transform[4] is pixel height
            pixel_width = abs(src_a.transform[0])
            pixel_height = abs(src_a.transform[4])
            pixel_area_sqm = pixel_width * pixel_height
            
            if pixel_area_sqm <= 0:
                raise ValueError("Invalid pixel area calculated from raster transform.")
                
    except rasterio.errors.RasterioIOError as e:
        raise FileNotFoundError(f"Error opening mask files: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error processing raster masks for change detection: {str(e)}")
        
    areas_year_a = calculate_area_from_mask(mask_a, pixel_area_sqm)
    areas_year_b = calculate_area_from_mask(mask_b, pixel_area_sqm)
    
    change_report = {}
    for cls in CLASSES.values():
        area_a = areas_year_a[cls]
        area_b = areas_year_b[cls]
        
        absolute_change = area_b - area_a
        if area_a > 0:
            percentage_change = (absolute_change / area_a) * 100
        else:
            percentage_change = float('inf') if area_b > 0 else 0.0
            
        change_report[cls] = {
            "area_year_a_sqkm": area_a,
            "area_year_b_sqkm": area_b,
            "absolute_change_sqkm": absolute_change,
            "percentage_change": percentage_change
        }
        
    return change_report

def format_report_for_llm(change_report, location_name, year_a, year_b):
    """
    Formats the change metrics to be fed into the LLM as a prompt.
    """
    prompt = f"Land cover change report for {location_name} between {year_a} and {year_b}:\n\n"
    for cls, metrics in change_report.items():
        prompt += f"- {cls}:\n"
        prompt += f"  - Area in {year_a}: {metrics['area_year_a_sqkm']:.2f} sq km\n"
        prompt += f"  - Area in {year_b}: {metrics['area_year_b_sqkm']:.2f} sq km\n"
        prompt += f"  - Absolute Change: {metrics['absolute_change_sqkm']:.2f} sq km\n"
        prompt += f"  - Percentage Change: {metrics['percentage_change']:.2f}%\n"
        
    prompt += "\nBased on this data, analyze the environmental impact and predict the possibility of any natural calamity occurrence (e.g., floods due to water body reduction or urban heat island effect due to building increase)."
    return prompt
