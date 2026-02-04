"""
Basic smoke tests for UI components.

These tests verify that UI components can be imported and basic
functionality works without Streamlit runtime errors.
"""

import json
from unittest.mock import MagicMock, patch
import sys


class TestUIComponentsImport:
    """Test that all UI components can be imported."""
    
    def test_import_india_map(self):
        """Test that india_map module can be imported."""
        import ui.india_map
        assert hasattr(ui.india_map, 'render_india_map')
        assert hasattr(ui.india_map, 'render_state_selector')
    
    def test_import_chat_panel(self):
        """Test that chat_panel module can be imported."""
        import ui.chat_panel
        assert hasattr(ui.chat_panel, 'render_chat_interface')
    
    def test_import_output_panels(self):
        """Test that output_panels module can be imported."""
        import ui.output_panels
        assert hasattr(ui.output_panels, 'render_time_selector')
        assert hasattr(ui.output_panels, 'render_analysis_output')


class TestStateDataLoading:
    """Test that state data can be loaded correctly."""
    
    def test_states_json_exists_and_valid(self):
        """Test that india_states.json exists and is valid JSON."""
        with open('data/india_states.json', 'r') as f:
            data = json.load(f)
        
        assert 'states' in data
        assert isinstance(data['states'], list)
        assert len(data['states']) > 0
    
    def test_states_have_required_fields(self):
        """Test that each state has name, latitude, and longitude."""
        with open('data/india_states.json', 'r') as f:
            data = json.load(f)
        
        for state in data['states']:
            assert 'name' in state
            assert 'latitude' in state
            assert 'longitude' in state
            assert isinstance(state['name'], str)
            assert isinstance(state['latitude'], (int, float))
            assert isinstance(state['longitude'], (int, float))
    
    def test_states_coordinates_within_india(self):
        """Test that all state coordinates are within India's boundaries."""
        with open('data/india_states.json', 'r') as f:
            data = json.load(f)
        
        for state in data['states']:
            lat = state['latitude']
            lon = state['longitude']
            assert 6 <= lat <= 37, f"{state['name']} latitude {lat} outside India boundaries"
            assert 68 <= lon <= 97, f"{state['name']} longitude {lon} outside India boundaries"
