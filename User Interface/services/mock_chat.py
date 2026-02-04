"""
Mock Chat Service

This module provides a mock implementation of the Chat Service API contract.
It generates context-aware responses that reference the selected state and time range.

The service is designed to be replaced with actual LLM models without requiring UI changes.
"""

from typing import Dict
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def chat(query: str, state: str, start_year: int, end_year: int) -> Dict:
    """
    Handle conversational queries with India-specific context.
    
    This is a mock implementation that generates context-aware responses.
    The response structure matches the Chat Service API contract exactly.
    
    Args:
        query: User's question or conversational input
        state: Selected Indian state or union territory for context
        start_year: Start year for temporal context (2019-2024)
        end_year: End year for temporal context (2019-2024)
        
    Returns:
        Dictionary containing:
        - response: Conversational answer incorporating context
        - context_used: Boolean indicating whether location and time context was applied
        
    Raises:
        ValueError: If required parameters are missing or invalid
    """
    try:
        # Log request (handle None query safely)
        query_preview = query[:50] if query else "None"
        logger.info(f"Chat request: query='{query_preview}...', state={state}, years={start_year}-{end_year}")
        
        # Parameter validation
        if query is None or query.strip() == "":
            logger.error("Missing or empty query parameter")
            raise ValueError("query is a required parameter and cannot be empty")
        
        if state is None or state.strip() == "":
            logger.error("Missing or empty state parameter")
            raise ValueError("state is a required parameter and cannot be empty")
        
        if start_year is None:
            logger.error("Missing start_year parameter")
            raise ValueError("start_year is a required parameter")
        
        if end_year is None:
            logger.error("Missing end_year parameter")
            raise ValueError("end_year is a required parameter")
        
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
        
        # Generate context-aware response
        query_lower = query.lower().strip()
        
        # Determine if context should be used based on query content
        context_keywords = [
            "state", "location", "area", "region", "here", "this place",
            "year", "time", "period", "when", "during", "between",
            state.lower()
        ]
        
        context_used = any(keyword in query_lower for keyword in context_keywords)
        
        # Generate response based on query type
        response_text = _generate_contextual_response(query_lower, state, start_year, end_year, context_used)
        
        # Construct response matching API contract
        response = {
            "response": response_text,
            "context_used": context_used
        }
        
        logger.info("Chat response generated successfully")
        return response
        
    except ValueError as e:
        # Re-raise ValueError for proper handling by caller
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat service: {str(e)}")
        raise RuntimeError(f"Chat service error: {str(e)}")


def _generate_contextual_response(query: str, state: str, start_year: int, end_year: int, use_context: bool) -> str:
    """
    Generate a contextual response based on the query and context.
    
    Args:
        query: Lowercase user query
        state: Selected state name
        start_year: Start year for context
        end_year: End year for context
        use_context: Whether to incorporate context in response
        
    Returns:
        Generated response string
    """
    # Seed random for deterministic responses based on query
    seed = sum(ord(c) for c in query) + start_year + end_year
    random.seed(seed)
    
    # Time range description
    if start_year == end_year:
        time_range = f"in {start_year}"
    else:
        time_range = f"between {start_year} and {end_year}"
    
    # Query pattern matching with context-aware responses
    if any(word in query for word in ["vegetation", "forest", "green", "tree"]):
        if use_context:
            responses = [
                f"Based on satellite data for {state} {time_range}, vegetation patterns show significant changes. "
                f"Forest cover in {state} has been affected by both natural and anthropogenic factors during this period.",
                f"Vegetation analysis for {state} {time_range} indicates variations in green cover. "
                f"The region has experienced changes in agricultural patterns and forest density.",
                f"In {state} {time_range}, vegetation health has been monitored through ISRO's satellite imagery. "
                f"The data shows seasonal variations and long-term trends in forest and agricultural areas."
            ]
        else:
            responses = [
                "Vegetation monitoring uses multispectral satellite imagery to track changes in forest cover, "
                "agricultural health, and green spaces over time.",
                "Forest cover analysis involves comparing satellite images across different time periods to "
                "identify deforestation, afforestation, and seasonal changes."
            ]
    
    elif any(word in query for word in ["water", "river", "lake", "reservoir", "flood"]):
        if use_context:
            responses = [
                f"Water body analysis for {state} {time_range} shows variations in surface water extent. "
                f"Rivers, lakes, and reservoirs in {state} have experienced changes due to rainfall patterns and water management.",
                f"For {state} {time_range}, satellite monitoring indicates fluctuations in water resources. "
                f"The region's water bodies have been affected by seasonal monsoons and human activities.",
                f"In {state} {time_range}, water resource monitoring through ISRO satellites reveals important trends. "
                f"Surface water extent has varied based on precipitation and water usage patterns."
            ]
        else:
            responses = [
                "Water body monitoring uses radar and optical satellite data to track changes in rivers, lakes, "
                "and reservoirs, helping with flood forecasting and water resource management.",
                "Satellite-based water monitoring can detect changes in surface water extent, helping identify "
                "drought conditions, flooding events, and long-term water availability trends."
            ]
    
    elif any(word in query for word in ["urban", "city", "built", "development", "construction"]):
        if use_context:
            responses = [
                f"Urban development in {state} {time_range} has been tracked through satellite imagery. "
                f"Built-up areas in {state} have expanded due to infrastructure projects and population growth.",
                f"For {state} {time_range}, urbanization patterns show significant changes. "
                f"The region has experienced growth in residential, commercial, and industrial areas.",
                f"In {state} {time_range}, urban expansion has been monitored using high-resolution satellite data. "
                f"Infrastructure development and city growth are clearly visible in the imagery."
            ]
        else:
            responses = [
                "Urban growth monitoring uses satellite imagery to track expansion of built-up areas, "
                "helping urban planners understand development patterns and infrastructure needs.",
                "Built-up area analysis involves detecting changes in construction, roads, and urban infrastructure "
                "over time using multispectral and radar satellite data."
            ]
    
    elif any(word in query for word in ["risk", "hazard", "danger", "threat"]):
        if use_context:
            responses = [
                f"Risk assessment for {state} {time_range} considers multiple environmental factors. "
                f"The region faces varying levels of flood risk, heat stress, and land degradation based on satellite observations.",
                f"For {state} {time_range}, environmental risk analysis indicates several concerns. "
                f"Satellite data helps identify areas vulnerable to natural hazards and climate impacts.",
                f"In {state} {time_range}, risk forecasting uses historical satellite data and current trends. "
                f"The analysis helps prioritize preventive measures for the most vulnerable areas."
            ]
        else:
            responses = [
                "Environmental risk assessment combines satellite observations with climate models to forecast "
                "potential hazards like floods, droughts, heat waves, and land degradation.",
                "Risk forecasting uses multi-temporal satellite data to identify trends and predict future "
                "environmental challenges, enabling proactive disaster management."
            ]
    
    elif any(word in query for word in ["climate", "weather", "temperature", "rainfall", "monsoon"]):
        if use_context:
            responses = [
                f"Climate patterns in {state} {time_range} have been analyzed using satellite and ground data. "
                f"The region experiences distinct seasonal variations with monsoon impacts on vegetation and water resources.",
                f"For {state} {time_range}, weather patterns show typical seasonal cycles. "
                f"Satellite data helps track temperature variations, rainfall distribution, and their environmental impacts.",
                f"In {state} {time_range}, climate monitoring reveals important trends. "
                f"The region's environmental conditions are influenced by monsoon patterns and temperature variations."
            ]
        else:
            responses = [
                "Climate monitoring combines satellite observations with meteorological data to track temperature, "
                "precipitation, and other weather parameters affecting environmental conditions.",
                "Weather pattern analysis uses satellite imagery to monitor cloud cover, rainfall, and temperature "
                "variations, helping understand climate impacts on ecosystems."
            ]
    
    elif any(word in query for word in ["satellite", "isro", "data", "imagery", "remote sensing"]):
        if use_context:
            responses = [
                f"ISRO satellite data for {state} {time_range} provides comprehensive environmental monitoring. "
                f"Multiple satellites including Resourcesat and Cartosat series capture high-resolution imagery of the region.",
                f"For {state} {time_range}, satellite observations come from ISRO's earth observation missions. "
                f"The data includes optical, thermal, and radar imagery for detailed environmental analysis.",
                f"In {state} {time_range}, remote sensing data from ISRO satellites enables detailed monitoring. "
                f"The imagery supports analysis of land use, water resources, and environmental changes."
            ]
        else:
            responses = [
                "ISRO operates multiple earth observation satellites including Resourcesat, Cartosat, and RISAT series "
                "that provide optical, thermal, and radar imagery for environmental monitoring across India.",
                "Satellite remote sensing uses electromagnetic radiation to capture images of Earth's surface, "
                "enabling monitoring of vegetation, water bodies, urban areas, and environmental changes."
            ]
    
    elif any(word in query for word in ["how", "what", "why", "explain", "tell me"]):
        if use_context:
            responses = [
                f"For {state} {time_range}, environmental analysis combines multiple data sources. "
                f"Satellite imagery, climate data, and ground observations are integrated to provide comprehensive insights about the region.",
                f"In {state} {time_range}, the analysis process involves processing satellite data through specialized algorithms. "
                f"This helps identify changes in land cover, water resources, and environmental conditions specific to the area.",
                f"Regarding {state} {time_range}, the system uses ISRO satellite data to track environmental parameters. "
                f"The analysis considers temporal changes and spatial patterns to generate insights for the selected region and time period."
            ]
        else:
            responses = [
                "Environmental analysis uses satellite imagery to detect changes in land cover, vegetation health, "
                "water resources, and urban development over time.",
                "The system processes multispectral satellite data to extract information about environmental conditions, "
                "identify trends, and forecast potential risks based on historical patterns."
            ]
    
    else:
        # Generic response for unmatched queries
        if use_context:
            responses = [
                f"Based on the analysis for {state} {time_range}, environmental monitoring provides valuable insights. "
                f"The satellite data for this region and time period helps understand various environmental parameters.",
                f"For {state} {time_range}, the system can provide information about environmental changes, "
                f"risk assessments, and trends specific to this region.",
                f"Regarding your query about {state} {time_range}, the environmental intelligence system uses "
                f"satellite data to analyze conditions and changes in the selected area during this period."
            ]
        else:
            responses = [
                "The India Earth-Observation Intelligence System provides environmental analysis, risk forecasting, "
                "and insights based on ISRO satellite data covering all regions of India.",
                "This system analyzes satellite imagery to monitor environmental changes, assess risks, "
                "and provide actionable insights for sustainable development and disaster management.",
                "Environmental intelligence combines satellite observations with analytical models to understand "
                "land use changes, water resources, vegetation health, and climate impacts across India."
            ]
    
    # Select a random response from the appropriate category
    return random.choice(responses)
