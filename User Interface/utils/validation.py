"""
Validation utilities for input validation and error checking.

This module provides validation functions for geographic coordinates,
time ranges, and other user inputs.
"""

from typing import Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# India's geographic boundaries
INDIA_MIN_LAT = 6.0
INDIA_MAX_LAT = 37.0
INDIA_MIN_LON = 68.0
INDIA_MAX_LON = 97.0

# Valid year range
MIN_YEAR = 2019
MAX_YEAR = 2024


def validate_coordinates(latitude: float, longitude: float) -> Tuple[bool, Optional[str]]:
    """
    Validate that coordinates are within India's boundaries.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if coordinates are valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if latitude is None or longitude is None:
        return False, "Latitude and longitude are required"
    
    try:
        lat = float(latitude)
        lon = float(longitude)
    except (ValueError, TypeError):
        return False, "Latitude and longitude must be numeric values"
    
    if not (INDIA_MIN_LAT <= lat <= INDIA_MAX_LAT):
        return False, f"Latitude must be between {INDIA_MIN_LAT}°N and {INDIA_MAX_LAT}°N (got {lat}°)"
    
    if not (INDIA_MIN_LON <= lon <= INDIA_MAX_LON):
        return False, f"Longitude must be between {INDIA_MIN_LON}°E and {INDIA_MAX_LON}°E (got {lon}°)"
    
    return True, None


def validate_time_range(start_year: int, end_year: int) -> Tuple[bool, Optional[str]]:
    """
    Validate that time range is valid.
    
    Args:
        start_year: Start year
        end_year: End year
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if time range is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if start_year is None or end_year is None:
        return False, "Start year and end year are required"
    
    try:
        start = int(start_year)
        end = int(end_year)
    except (ValueError, TypeError):
        return False, "Start year and end year must be integers"
    
    if not (MIN_YEAR <= start <= MAX_YEAR):
        return False, f"Start year must be between {MIN_YEAR} and {MAX_YEAR} (got {start})"
    
    if not (MIN_YEAR <= end <= MAX_YEAR):
        return False, f"End year must be between {MIN_YEAR} and {MAX_YEAR} (got {end})"
    
    if start > end:
        return False, f"Start year ({start}) cannot be after end year ({end})"
    
    return True, None


def validate_state_name(state: str) -> Tuple[bool, Optional[str]]:
    """
    Validate that state name is not empty.
    
    Args:
        state: State name
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if state name is valid, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if state is None:
        return False, "State name is required"
    
    if not isinstance(state, str):
        return False, "State name must be a string"
    
    if state.strip() == "" or state == "-- Select a State --":
        return False, "Please select a valid state"
    
    return True, None


def validate_location_selected(location: Optional[dict]) -> Tuple[bool, Optional[str]]:
    """
    Validate that a location has been selected.
    
    Args:
        location: Location dictionary with latitude and longitude
        
    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if location is selected, False otherwise
        - error_message: None if valid, error description if invalid
    """
    if location is None:
        return False, "Please select a location (click on map or choose from dropdown)"
    
    if not isinstance(location, dict):
        return False, "Invalid location format"
    
    if "latitude" not in location or "longitude" not in location:
        return False, "Location must contain latitude and longitude"
    
    # Validate the coordinates
    return validate_coordinates(location["latitude"], location["longitude"])
