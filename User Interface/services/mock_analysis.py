"""
Mock Analysis Service

This module provides a mock implementation of the Analysis Service API contract.
It generates realistic sample data for environmental analysis based on input parameters.

The service is designed to be replaced with actual ML models without requiring UI changes.
"""

from typing import Dict, List
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze(latitude: float, longitude: float, start_year: int, end_year: int) -> Dict:
    """
    Analyze environmental changes for a given location and time range.
    
    This is a mock implementation that generates realistic sample data.
    The response structure matches the Analysis Service API contract exactly.
    
    Args:
        latitude: Location latitude (must be within 6°N-37°N for India)
        longitude: Location longitude (must be within 68°E-97°E for India)
        start_year: Analysis start year (2019-2024)
        end_year: Analysis end year (2019-2024)
        
    Returns:
        Dictionary containing:
        - environmental_changes: vegetation, water, and built-up area percentage changes
        - risk_forecast: flood, heat stress, and land degradation risk levels
        - preventive_actions: categorized by time horizon (immediate, medium_term, long_term)
        
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    try:
        logger.info(f"Analysis request: lat={latitude}, lon={longitude}, years={start_year}-{end_year}")
        
        # Parameter validation
        if latitude is None or longitude is None:
            logger.error("Missing required parameters: latitude or longitude")
            raise ValueError("latitude and longitude are required parameters")
        
        if start_year is None or end_year is None:
            logger.error("Missing required parameters: start_year or end_year")
            raise ValueError("start_year and end_year are required parameters")
        
        # Validate geographic boundaries (India)
        if not (6 <= latitude <= 37):
            logger.error(f"Invalid latitude: {latitude} (must be between 6°N and 37°N)")
            raise ValueError(f"latitude must be between 6°N and 37°N, got {latitude}")
        
        if not (68 <= longitude <= 97):
            logger.error(f"Invalid longitude: {longitude} (must be between 68°E and 97°E)")
            raise ValueError(f"longitude must be between 68°E and 97°E, got {longitude}")
        
        # Validate year range
        if not (2019 <= start_year <= 2024):
            logger.error(f"Invalid start_year: {start_year} (must be between 2019 and 2024)")
            raise ValueError(f"start_year must be between 2019 and 2024, got {start_year}")
        
        if not (2019 <= end_year <= 2024):
            logger.error(f"Invalid end_year: {end_year} (must be between 2019 and 2024)")
            raise ValueError(f"end_year must be between 2019 and 2024, got {end_year}")
        
        if start_year > end_year:
            logger.error(f"Invalid time range: start_year ({start_year}) > end_year ({end_year})")
            raise ValueError(f"start_year ({start_year}) cannot be after end_year ({end_year})")
        
        # Generate realistic mock data based on input parameters
        # Use location and time range to create deterministic but varied results
        seed = int((latitude * 1000 + longitude * 100 + start_year + end_year))
        random.seed(seed)
        
        # Calculate time span for scaling changes
        time_span = end_year - start_year + 1
        
        # Environmental changes (percentage changes scaled by time span)
        vegetation_change = round(random.uniform(-15, 10) * (time_span / 5), 2)
        water_change = round(random.uniform(-8, 5) * (time_span / 5), 2)
        built_up_change = round(random.uniform(0, 20) * (time_span / 5), 2)
        
        # Risk levels based on location characteristics
        # Northern regions: higher flood risk
        # Southern regions: higher heat stress
        # Central regions: higher land degradation
        risk_levels = ["Low", "Medium", "High"]
        
        if latitude > 28:  # Northern India
            flood_risk = random.choice(["Medium", "High"])
            heat_stress_risk = random.choice(["Low", "Medium"])
            land_degradation_risk = random.choice(["Low", "Medium"])
        elif latitude < 15:  # Southern India
            flood_risk = random.choice(["Low", "Medium"])
            heat_stress_risk = random.choice(["Medium", "High"])
            land_degradation_risk = random.choice(["Low", "Medium"])
        else:  # Central India
            flood_risk = random.choice(["Low", "Medium"])
            heat_stress_risk = random.choice(["Medium", "High"])
            land_degradation_risk = random.choice(["Medium", "High"])
        
        # Preventive actions based on identified risks
        immediate_actions = []
        medium_term_actions = []
        long_term_actions = []
        
        # Add actions based on risk levels
        if flood_risk in ["Medium", "High"]:
            immediate_actions.append("Monitor water levels and weather forecasts")
            medium_term_actions.append("Improve drainage infrastructure")
            long_term_actions.append("Develop flood-resistant urban planning")
        
        if heat_stress_risk in ["Medium", "High"]:
            immediate_actions.append("Issue heat wave warnings to vulnerable populations")
            medium_term_actions.append("Increase urban green cover")
            long_term_actions.append("Implement climate-resilient building codes")
        
        if land_degradation_risk in ["Medium", "High"]:
            immediate_actions.append("Restrict deforestation activities")
            medium_term_actions.append("Promote soil conservation practices")
            long_term_actions.append("Implement sustainable land management policies")
        
        # Add general actions
        if not immediate_actions:
            immediate_actions.append("Continue environmental monitoring")
        
        medium_term_actions.append("Conduct detailed environmental impact assessments")
        long_term_actions.append("Develop comprehensive climate adaptation strategy")
        
        # Construct response matching API contract
        response = {
            "environmental_changes": {
                "vegetation_change": vegetation_change,
                "water_change": water_change,
                "built_up_change": built_up_change
            },
            "risk_forecast": {
                "flood_risk": flood_risk,
                "heat_stress_risk": heat_stress_risk,
                "land_degradation_risk": land_degradation_risk
            },
            "preventive_actions": {
                "immediate": immediate_actions,
                "medium_term": medium_term_actions,
                "long_term": long_term_actions
            }
        }
        
        logger.info("Analysis completed successfully")
        return response
        
    except ValueError as e:
        # Re-raise ValueError for proper handling by caller
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analysis service: {str(e)}")
        raise RuntimeError(f"Analysis service error: {str(e)}")
