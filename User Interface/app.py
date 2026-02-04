"""
India Earth-Observation Intelligence System

Main Streamlit application providing environmental analysis, risk forecasting,
and conversational intelligence for locations within India using ISRO satellite data.
"""

import os
import streamlit as st
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import logging
from ui.india_map import render_india_map, render_state_selector
from ui.output_panels import render_time_selector, render_analysis_output
from ui.chat_panel import render_chat_interface
from services.mock_analysis import analyze
from utils.validation import validate_location_selected, validate_time_range

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Page configuration
st.set_page_config(
    page_title="India EO Intelligence System",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to ensure button text visibility
st.markdown("""
    <style>
    /* Ensure primary button text is visible */
    .stButton > button[kind="primary"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #E0E0E0 !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

if "selected_state" not in st.session_state:
    st.session_state.selected_state = None

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "start_year" not in st.session_state:
    st.session_state.start_year = 2019

if "end_year" not in st.session_state:
    st.session_state.end_year = 2024


# Application header
st.title("🛰️ India Earth-Observation Intelligence System")
st.markdown(
    """
    Analyze environmental changes, assess risks, and explore insights using ISRO satellite data.
    Select a location on the map or choose a state, then click **Analyze** to begin.
    """
)

st.divider()

# Sidebar - Location Selection
with st.sidebar:
    st.header("📍 Location Selection")
    
    # State selector dropdown
    state_selection = render_state_selector()
    
    if state_selection:
        state_name, state_lat, state_lon = state_selection
        st.session_state.selected_state = state_name
        st.session_state.selected_location = {
            "latitude": state_lat,
            "longitude": state_lon
        }
        st.success(f"Selected: {state_name}")
        st.caption(f"Coordinates: {state_lat:.4f}°N, {state_lon:.4f}°E")
    
    st.markdown("**OR**")
    st.caption("Click on the map below to select a location")
    
    st.divider()
    
    # Time range selection
    st.header("📅 Time Range")
    start_year, end_year = render_time_selector()
    st.session_state.start_year = start_year
    st.session_state.end_year = end_year
    
    st.divider()
    
    # Analyze button
    analyze_button = st.button("🔍 Analyze", type="primary", use_container_width=True)
    
    if analyze_button:
        # Validate location is selected
        is_valid_location, location_error = validate_location_selected(st.session_state.selected_location)
        
        if not is_valid_location:
            logger.warning(f"Location validation failed: {location_error}")
            st.warning(f"⚠️ {location_error}")
        else:
            # Validate time range
            is_valid_time, time_error = validate_time_range(
                st.session_state.start_year,
                st.session_state.end_year
            )
            
            if not is_valid_time:
                logger.warning(f"Time range validation failed: {time_error}")
                st.error(f"❌ {time_error}")
            else:
                try:
                    with st.spinner("Analyzing environmental data..."):
                        # Call analysis service with timeout handling
                        with ThreadPoolExecutor(max_workers=1) as executor:
                            future = executor.submit(
                                analyze,
                                latitude=st.session_state.selected_location["latitude"],
                                longitude=st.session_state.selected_location["longitude"],
                                start_year=st.session_state.start_year,
                                end_year=st.session_state.end_year
                            )
                            
                            try:
                                # Wait for result with 5 second timeout
                                analysis_data = future.result(timeout=5.0)
                                
                                # Store results in session state
                                st.session_state.analysis_results = analysis_data
                                st.success("✅ Analysis complete!")
                                logger.info("Analysis completed successfully")
                                
                            except TimeoutError:
                                logger.error("Analysis service timeout")
                                st.error("⏱️ Service timeout: The analysis is taking too long. Please try again.")
                            except Exception as e:
                                logger.error(f"Error during analysis execution: {str(e)}")
                                raise
                    
                except ValueError as e:
                    logger.error(f"Validation error: {str(e)}")
                    st.error(f"❌ Validation error: {str(e)}")
                except RuntimeError as e:
                    logger.error(f"Service error: {str(e)}")
                    st.error(f"❌ Service error: {str(e)}")
                except Exception as e:
                    logger.error(f"Unexpected error during analysis: {str(e)}")
                    st.error(f"❌ An unexpected error occurred. Please try again or contact support.")


# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🗺️ India Map")
    
    # Render map with selected state highlighted
    map_click = render_india_map(
        selected_state=st.session_state.selected_state
    )
    
    # Handle map click
    if map_click:
        st.session_state.selected_location = map_click
        st.session_state.selected_state = None  # Clear state selection when map is clicked
        st.success(
            f"Location selected: {map_click['latitude']:.4f}°N, {map_click['longitude']:.4f}°E"
        )
        st.rerun()

with col2:
    st.subheader("📊 Current Selection")
    
    if st.session_state.selected_location:
        st.info(
            f"""
            **Location:** {st.session_state.selected_state or 'Custom Location'}  
            **Coordinates:** {st.session_state.selected_location['latitude']:.4f}°N, 
            {st.session_state.selected_location['longitude']:.4f}°E  
            **Time Range:** {st.session_state.start_year} - {st.session_state.end_year}
            """
        )
    else:
        st.info("No location selected. Please select a location to begin analysis.")

st.divider()

# Analysis results display
if st.session_state.analysis_results:
    render_analysis_output(st.session_state.analysis_results)
    
    st.divider()
    
    # Chat interface (only show if analysis has been performed)
    if st.session_state.selected_state or st.session_state.selected_location:
        # Determine state name for context
        context_state = st.session_state.selected_state or "Selected Location"
        
        render_chat_interface(
            state=context_state,
            start_year=st.session_state.start_year,
            end_year=st.session_state.end_year
        )
else:
    st.info("👆 Select a location and click **Analyze** to view environmental analysis and access the chat assistant.")

# Footer
st.divider()
version = "1.0.0"
commit_hash = os.getenv("COMMIT_SHA", "dev")[:7]
st.caption(
    f"**Version {version}** | **Commit {commit_hash}** | **Data Source:** ISRO (Indian Space Research Organisation)"
)
