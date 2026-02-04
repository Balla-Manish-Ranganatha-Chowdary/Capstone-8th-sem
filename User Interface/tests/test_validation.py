"""
Tests for validation utilities.

This module tests the validation functions for coordinates, time ranges,
and other user inputs.
"""

import pytest
from utils.validation import (
    validate_coordinates,
    validate_time_range,
    validate_state_name,
    validate_location_selected
)


class TestCoordinateValidation:
    """Test coordinate validation functions."""
    
    def test_valid_coordinates(self):
        """Test that valid coordinates within India's boundaries are accepted."""
        is_valid, error = validate_coordinates(20.5937, 78.9629)
        assert is_valid is True
        assert error is None
    
    def test_coordinates_at_boundaries(self):
        """Test coordinates at exact boundary values."""
        # Min boundaries
        is_valid, error = validate_coordinates(6.0, 68.0)
        assert is_valid is True
        
        # Max boundaries
        is_valid, error = validate_coordinates(37.0, 97.0)
        assert is_valid is True
    
    def test_latitude_below_boundary(self):
        """Test that latitude below India's boundary is rejected."""
        is_valid, error = validate_coordinates(5.0, 78.0)
        assert is_valid is False
        assert "Latitude must be between" in error
    
    def test_latitude_above_boundary(self):
        """Test that latitude above India's boundary is rejected."""
        is_valid, error = validate_coordinates(38.0, 78.0)
        assert is_valid is False
        assert "Latitude must be between" in error
    
    def test_longitude_below_boundary(self):
        """Test that longitude below India's boundary is rejected."""
        is_valid, error = validate_coordinates(20.0, 67.0)
        assert is_valid is False
        assert "Longitude must be between" in error
    
    def test_longitude_above_boundary(self):
        """Test that longitude above India's boundary is rejected."""
        is_valid, error = validate_coordinates(20.0, 98.0)
        assert is_valid is False
        assert "Longitude must be between" in error
    
    def test_none_coordinates(self):
        """Test that None coordinates are rejected."""
        is_valid, error = validate_coordinates(None, 78.0)
        assert is_valid is False
        assert "required" in error.lower()
        
        is_valid, error = validate_coordinates(20.0, None)
        assert is_valid is False
        assert "required" in error.lower()


class TestTimeRangeValidation:
    """Test time range validation functions."""
    
    def test_valid_time_range(self):
        """Test that valid time range is accepted."""
        is_valid, error = validate_time_range(2019, 2024)
        assert is_valid is True
        assert error is None
    
    def test_same_year_range(self):
        """Test that same start and end year is valid."""
        is_valid, error = validate_time_range(2020, 2020)
        assert is_valid is True
        assert error is None
    
    def test_start_year_after_end_year(self):
        """Test that start year after end year is rejected."""
        is_valid, error = validate_time_range(2024, 2019)
        assert is_valid is False
        assert "cannot be after" in error
    
    def test_year_below_range(self):
        """Test that year below valid range is rejected."""
        is_valid, error = validate_time_range(2018, 2024)
        assert is_valid is False
        assert "must be between" in error
    
    def test_year_above_range(self):
        """Test that year above valid range is rejected."""
        is_valid, error = validate_time_range(2019, 2025)
        assert is_valid is False
        assert "must be between" in error
    
    def test_none_years(self):
        """Test that None years are rejected."""
        is_valid, error = validate_time_range(None, 2024)
        assert is_valid is False
        assert "required" in error.lower()
        
        is_valid, error = validate_time_range(2019, None)
        assert is_valid is False
        assert "required" in error.lower()


class TestStateNameValidation:
    """Test state name validation functions."""
    
    def test_valid_state_name(self):
        """Test that valid state name is accepted."""
        is_valid, error = validate_state_name("Delhi")
        assert is_valid is True
        assert error is None
    
    def test_empty_state_name(self):
        """Test that empty state name is rejected."""
        is_valid, error = validate_state_name("")
        assert is_valid is False
        assert "select a valid state" in error.lower()
    
    def test_placeholder_state_name(self):
        """Test that placeholder state name is rejected."""
        is_valid, error = validate_state_name("-- Select a State --")
        assert is_valid is False
        assert "select a valid state" in error.lower()
    
    def test_none_state_name(self):
        """Test that None state name is rejected."""
        is_valid, error = validate_state_name(None)
        assert is_valid is False
        assert "required" in error.lower()


class TestLocationValidation:
    """Test location validation functions."""
    
    def test_valid_location(self):
        """Test that valid location dictionary is accepted."""
        location = {"latitude": 20.5937, "longitude": 78.9629}
        is_valid, error = validate_location_selected(location)
        assert is_valid is True
        assert error is None
    
    def test_none_location(self):
        """Test that None location is rejected."""
        is_valid, error = validate_location_selected(None)
        assert is_valid is False
        assert "select a location" in error.lower()
    
    def test_missing_latitude(self):
        """Test that location missing latitude is rejected."""
        location = {"longitude": 78.9629}
        is_valid, error = validate_location_selected(location)
        assert is_valid is False
        assert "latitude and longitude" in error.lower()
    
    def test_missing_longitude(self):
        """Test that location missing longitude is rejected."""
        location = {"latitude": 20.5937}
        is_valid, error = validate_location_selected(location)
        assert is_valid is False
        assert "latitude and longitude" in error.lower()
    
    def test_invalid_coordinates_in_location(self):
        """Test that location with invalid coordinates is rejected."""
        location = {"latitude": 50.0, "longitude": 78.9629}
        is_valid, error = validate_location_selected(location)
        assert is_valid is False
        assert "must be between" in error
