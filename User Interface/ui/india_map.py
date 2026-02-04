"""
India Map Component

This module provides interactive map visualization and state selection
for the India Earth-Observation Intelligence System.
"""

import json
import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import Optional, Dict, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_india_map(selected_state: Optional[str] = None) -> Dict[str, float]:
    """
    Renders an interactive map of India with state boundaries.
    
    The map is styled with a black background and white boundaries for
    high contrast. Click events are captured to allow location selection.
    Map bounds are restricted to India's geographic boundaries.
    
    Args:
        selected_state: Optional state name to highlight on the map
        
    Returns:
        Dictionary with 'latitude' and 'longitude' keys if a location
        was clicked, empty dict otherwise
    """
    # India's geographic center for initial map view
    india_center = [20.5937, 78.9629]
    
    # Create map with custom styling
    m = folium.Map(
        location=india_center,
        zoom_start=5,
        tiles=None,  # No default tiles, we'll add custom ones
        max_bounds=True,
        min_lat=6.0,
        max_lat=37.0,
        min_lon=68.0,
        max_lon=97.0,
        min_zoom=5,
        max_zoom=10
    )
    
    # Add dark tile layer for black background
    folium.TileLayer(
        tiles='https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
        name='Dark Map',
        overlay=False,
        control=False
    ).add_to(m)
    
    # Add India boundary rectangle to visualize the constraint
    folium.Rectangle(
        bounds=[[6.0, 68.0], [37.0, 97.0]],
        color='#FFFFFF',
        weight=2,
        fill=False,
        popup='India Boundaries'
    ).add_to(m)
    
    # If a state is selected, add a marker
    if selected_state:
        # Load state coordinates
        try:
            with open('data/india_states.json', 'r') as f:
                states_data = json.load(f)
                for state in states_data['states']:
                    if state['name'] == selected_state:
                        folium.Marker(
                            location=[state['latitude'], state['longitude']],
                            popup=state['name'],
                            icon=folium.Icon(color='red', icon='info-sign')
                        ).add_to(m)
                        break
        except FileNotFoundError:
            logger.error("State data file not found")
            st.error("❌ State data file not found. Please ensure data/india_states.json exists.")
        except json.JSONDecodeError:
            logger.error("Invalid JSON in state data file")
            st.error("❌ Invalid state data file format.")
        except Exception as e:
            logger.error(f"Error loading state data: {str(e)}")
            st.error(f"❌ Error loading state data: {str(e)}")
    
    # Render map and capture click events
    try:
        map_data = st_folium(
            m,
            width=700,
            height=500,
            returned_objects=["last_clicked"]
        )
    except Exception as e:
        logger.error(f"Error rendering map: {str(e)}")
        st.error("❌ Map visualization unavailable. Please use state selector dropdown.")
        return {}
    
    # Extract clicked coordinates if available
    result = {}
    if map_data and map_data.get("last_clicked"):
        clicked = map_data["last_clicked"]
        lat = clicked.get("lat")
        lon = clicked.get("lng")
        
        if lat is not None and lon is not None:
            # Validate coordinates are within India's boundaries
            if 6.0 <= lat <= 37.0 and 68.0 <= lon <= 97.0:
                result = {"latitude": lat, "longitude": lon}
                logger.info(f"Valid location selected: {lat}, {lon}")
            else:
                logger.warning(f"Location outside India's boundaries: {lat}, {lon}")
                st.error("❌ Selected location is outside India's boundaries (6°N-37°N, 68°E-97°E)")
    
    return result


def render_state_selector() -> Optional[Tuple[str, float, float]]:
    """
    Renders a dropdown for selecting Indian states and union territories.
    
    Loads state data from data/india_states.json and provides a selectbox
    for users to choose a state. Returns the state name and its coordinates.
    
    Returns:
        Tuple of (state_name, latitude, longitude) if a state is selected,
        None otherwise
    """
    try:
        # Load states data
        with open('data/india_states.json', 'r') as f:
            states_data = json.load(f)
        
        # Validate data structure
        if 'states' not in states_data:
            logger.error("Invalid state data structure: missing 'states' key")
            st.error("❌ Invalid state data file structure.")
            return None
        
        # Extract state names
        state_names = [state['name'] for state in states_data['states']]
        
        if not state_names:
            logger.error("No states found in data file")
            st.error("❌ No states found in data file.")
            return None
        
        # Create dropdown with placeholder
        selected_state = st.selectbox(
            "Select a State or Union Territory",
            options=["-- Select a State --"] + state_names,
            index=0
        )
        
        # Return state data if a valid state is selected
        if selected_state != "-- Select a State --":
            for state in states_data['states']:
                if state['name'] == selected_state:
                    # Validate state coordinates
                    lat = state.get('latitude')
                    lon = state.get('longitude')
                    
                    if lat is None or lon is None:
                        logger.error(f"Missing coordinates for state: {selected_state}")
                        st.error(f"❌ Invalid data for state: {selected_state}")
                        return None
                    
                    # Validate coordinates are within India's boundaries
                    if not (6.0 <= lat <= 37.0 and 68.0 <= lon <= 97.0):
                        logger.error(f"Coordinates outside India's boundaries for state: {selected_state}")
                        st.error(f"❌ Invalid coordinates for state: {selected_state}")
                        return None
                    
                    logger.info(f"State selected: {selected_state}")
                    return (state['name'], lat, lon)
        
        return None
        
    except FileNotFoundError:
        logger.error("State data file not found: data/india_states.json")
        st.error("❌ State data file not found. Please ensure data/india_states.json exists.")
        return None
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in state data file: {str(e)}")
        st.error("❌ Invalid state data file format. Please check the JSON structure.")
        return None
    except KeyError as e:
        logger.error(f"Missing required field in state data: {str(e)}")
        st.error(f"❌ Invalid state data: missing required field {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading state data: {str(e)}")
        st.error(f"❌ Error loading state data: {str(e)}")
        return None
