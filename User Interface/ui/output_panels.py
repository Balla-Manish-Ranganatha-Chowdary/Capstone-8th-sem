"""
Output panels component for displaying time selection and analysis results.

This module provides UI components for:
- Time range selection with validation
- Analysis results display including environmental changes, risk forecasts, and preventive actions
"""

from typing import Dict, Tuple
import streamlit as st
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_time_selector() -> Tuple[int, int]:
    """
    Renders year selection dropdowns for analysis time range.
    
    Provides two dropdowns for selecting start and end years (2019-2024).
    Validates that start_year <= end_year and displays warning if invalid.
    
    Returns:
        Tuple of (start_year, end_year) with validated years
    """
    col1, col2 = st.columns(2)
    
    with col1:
        start_year = st.selectbox(
            "Start Year",
            options=list(range(2019, 2025)),
            index=0,
            key="start_year_selector"
        )
    
    with col2:
        end_year = st.selectbox(
            "End Year",
            options=list(range(2019, 2025)),
            index=5,
            key="end_year_selector"
        )
    
    # Validate time range
    if start_year > end_year:
        logger.warning(f"Invalid time range: start_year ({start_year}) > end_year ({end_year})")
        st.warning("⚠️ Start year cannot be after end year. Please adjust your selection.")
        # Auto-correct by swapping
        start_year, end_year = end_year, start_year
        logger.info(f"Auto-corrected time range to: {start_year}-{end_year}")
    
    return start_year, end_year


def render_analysis_output(analysis_data: Dict) -> None:
    """
    Renders analysis results including environmental changes, risk forecasts, and preventive actions.
    
    Args:
        analysis_data: Dictionary matching Analysis Service response contract with keys:
            - environmental_changes: dict with vegetation_change, water_change, built_up_change
            - risk_forecast: dict with flood_risk, heat_stress_risk, land_degradation_risk
            - preventive_actions: dict with immediate, medium_term, long_term lists
    """
    if not analysis_data:
        st.info("No analysis data available. Please select a location and click Analyze.")
        return
    
    try:
        # Environmental Changes Section
        st.subheader("🌍 Environmental Changes")
        
        env_changes = analysis_data.get("environmental_changes", {})
        
        if not env_changes:
            logger.warning("Missing environmental_changes in analysis data")
            st.warning("⚠️ Environmental changes data not available.")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                veg_change = env_changes.get("vegetation_change", 0)
                st.metric(
                    label="Vegetation Change",
                    value=f"{veg_change:+.1f}%",
                    delta=f"{veg_change:.1f}%"
                )
            
            with col2:
                water_change = env_changes.get("water_change", 0)
                st.metric(
                    label="Water Bodies Change",
                    value=f"{water_change:+.1f}%",
                    delta=f"{water_change:.1f}%"
                )
            
            with col3:
                built_up_change = env_changes.get("built_up_change", 0)
                st.metric(
                    label="Built-up Area Change",
                    value=f"{built_up_change:+.1f}%",
                    delta=f"{built_up_change:.1f}%"
                )
        
        st.divider()
        
        # Risk Forecast Section
        st.subheader("⚠️ Risk Forecast")
        
        risk_forecast = analysis_data.get("risk_forecast", {})
        
        if not risk_forecast:
            logger.warning("Missing risk_forecast in analysis data")
            st.warning("⚠️ Risk forecast data not available.")
        else:
            # Helper function to get color based on severity
            def get_risk_color(severity: str) -> str:
                severity_lower = severity.lower()
                if severity_lower == "high":
                    return "🔴"
                elif severity_lower == "medium":
                    return "🟡"
                else:
                    return "🟢"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                flood_risk = risk_forecast.get("flood_risk", "Low")
                st.markdown(f"**Flood Risk**")
                st.markdown(f"{get_risk_color(flood_risk)} {flood_risk}")
            
            with col2:
                heat_stress_risk = risk_forecast.get("heat_stress_risk", "Low")
                st.markdown(f"**Heat Stress Risk**")
                st.markdown(f"{get_risk_color(heat_stress_risk)} {heat_stress_risk}")
            
            with col3:
                land_degradation_risk = risk_forecast.get("land_degradation_risk", "Low")
                st.markdown(f"**Land Degradation Risk**")
                st.markdown(f"{get_risk_color(land_degradation_risk)} {land_degradation_risk}")
        
        st.divider()
        
        # Preventive Actions Section
        st.subheader("🛡️ Preventive Actions")
        
        preventive_actions = analysis_data.get("preventive_actions", {})
        
        if not preventive_actions:
            logger.warning("Missing preventive_actions in analysis data")
            st.warning("⚠️ Preventive actions data not available.")
        else:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**Immediate Actions**")
                immediate_actions = preventive_actions.get("immediate", [])
                if immediate_actions:
                    for action in immediate_actions:
                        st.markdown(f"• {action}")
                else:
                    st.markdown("_No immediate actions required_")
            
            with col2:
                st.markdown("**Medium-term Actions**")
                medium_term_actions = preventive_actions.get("medium_term", [])
                if medium_term_actions:
                    for action in medium_term_actions:
                        st.markdown(f"• {action}")
                else:
                    st.markdown("_No medium-term actions required_")
            
            with col3:
                st.markdown("**Long-term Actions**")
                long_term_actions = preventive_actions.get("long_term", [])
                if long_term_actions:
                    for action in long_term_actions:
                        st.markdown(f"• {action}")
                else:
                    st.markdown("_No long-term actions required_")
    
    except Exception as e:
        logger.error(f"Error rendering analysis output: {str(e)}")
        st.error(f"❌ Error displaying analysis results: {str(e)}")
