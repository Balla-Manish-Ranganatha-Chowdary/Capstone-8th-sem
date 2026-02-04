"""
Chat Interface Component

This module provides the chat interface for conversational interaction with the system.
The chat maintains history and incorporates location and time context in queries.
"""

import streamlit as st
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import logging
from services.mock_chat import chat
from utils.validation import validate_state_name, validate_time_range

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def render_chat_interface(state: str, start_year: int, end_year: int) -> None:
    """
    Renders the chat interface with history and input.
    
    Displays a chat history window and provides a text input for user queries.
    All queries are sent to the chat service with the current state and time range context.
    
    Args:
        state: Currently selected state for context
        start_year: Start year for context
        end_year: End year for context
    """
    # Initialize chat history in session state if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat header
    st.subheader("💬 Chat Assistant")
    st.caption(f"Context: {state} | {start_year}-{end_year}")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        if len(st.session_state.chat_history) == 0:
            st.info("👋 Ask me anything about environmental data, satellite imagery, or analysis for the selected region!")
        else:
            for message in st.session_state.chat_history:
                role = message["role"]
                content = message["content"]
                
                if role == "user":
                    with st.chat_message("user"):
                        st.write(content)
                else:  # assistant
                    with st.chat_message("assistant"):
                        st.write(content)
    
    # Chat input
    user_query = st.chat_input("Ask a question about environmental data...")
    
    if user_query:
        # Validate inputs before making service call
        is_valid_state, state_error = validate_state_name(state)
        is_valid_time, time_error = validate_time_range(start_year, end_year)
        
        if not is_valid_state:
            logger.warning(f"State validation failed: {state_error}")
            st.error(f"❌ {state_error}")
            return
        
        if not is_valid_time:
            logger.warning(f"Time range validation failed: {time_error}")
            st.error(f"❌ {time_error}")
            return
        
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_query
        })
        
        # Call chat service with context and timeout handling
        try:
            with ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(
                    chat,
                    query=user_query,
                    state=state,
                    start_year=start_year,
                    end_year=end_year
                )
                
                try:
                    # Wait for result with 5 second timeout
                    response_data = future.result(timeout=5.0)
                    
                    # Extract response text
                    assistant_response = response_data["response"]
                    
                    # Add assistant response to history
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": assistant_response
                    })
                    
                    logger.info("Chat response generated successfully")
                    
                    # Rerun to display new messages
                    st.rerun()
                    
                except TimeoutError:
                    logger.error("Chat service timeout")
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "⏱️ Sorry, the response is taking too long. Please try again."
                    })
                    st.rerun()
                    
        except ValueError as e:
            logger.error(f"Validation error in chat: {str(e)}")
            st.error(f"❌ Validation error: {str(e)}")
        except RuntimeError as e:
            logger.error(f"Chat service error: {str(e)}")
            st.error(f"❌ Service error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error in chat: {str(e)}")
            st.error(f"❌ An unexpected error occurred. Please try again.")
