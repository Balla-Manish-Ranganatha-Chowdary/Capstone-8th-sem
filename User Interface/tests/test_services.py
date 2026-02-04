"""
Unit tests for mock backend services.

Tests verify that mock_analysis and mock_chat services:
- Accept valid inputs and return correct response structures
- Validate required parameters
- Handle boundary conditions appropriately
- Match API contract specifications
"""

import pytest
import json
from services.mock_analysis import analyze
from services.mock_chat import chat


class TestAnalysisService:
    """Tests for the mock analysis service."""
    
    def test_analyze_valid_input(self):
        """Test that analyze() returns correct structure with valid inputs."""
        result = analyze(
            latitude=28.6139,  # Delhi
            longitude=77.2090,
            start_year=2019,
            end_year=2024
        )
        
        # Verify response structure
        assert "environmental_changes" in result
        assert "risk_forecast" in result
        assert "preventive_actions" in result
        
        # Verify environmental_changes fields
        env_changes = result["environmental_changes"]
        assert "vegetation_change" in env_changes
        assert "water_change" in env_changes
        assert "built_up_change" in env_changes
        assert isinstance(env_changes["vegetation_change"], (int, float))
        assert isinstance(env_changes["water_change"], (int, float))
        assert isinstance(env_changes["built_up_change"], (int, float))
        
        # Verify risk_forecast fields
        risk = result["risk_forecast"]
        assert "flood_risk" in risk
        assert "heat_stress_risk" in risk
        assert "land_degradation_risk" in risk
        assert risk["flood_risk"] in ["Low", "Medium", "High"]
        assert risk["heat_stress_risk"] in ["Low", "Medium", "High"]
        assert risk["land_degradation_risk"] in ["Low", "Medium", "High"]
        
        # Verify preventive_actions fields
        actions = result["preventive_actions"]
        assert "immediate" in actions
        assert "medium_term" in actions
        assert "long_term" in actions
        assert isinstance(actions["immediate"], list)
        assert isinstance(actions["medium_term"], list)
        assert isinstance(actions["long_term"], list)
        assert len(actions["immediate"]) > 0
        assert len(actions["medium_term"]) > 0
        assert len(actions["long_term"]) > 0
    
    def test_analyze_missing_latitude(self):
        """Test that analyze() raises error when latitude is missing."""
        with pytest.raises(ValueError, match="latitude and longitude are required"):
            analyze(latitude=None, longitude=77.2090, start_year=2019, end_year=2024)
    
    def test_analyze_missing_longitude(self):
        """Test that analyze() raises error when longitude is missing."""
        with pytest.raises(ValueError, match="latitude and longitude are required"):
            analyze(latitude=28.6139, longitude=None, start_year=2019, end_year=2024)
    
    def test_analyze_missing_start_year(self):
        """Test that analyze() raises error when start_year is missing."""
        with pytest.raises(ValueError, match="start_year and end_year are required"):
            analyze(latitude=28.6139, longitude=77.2090, start_year=None, end_year=2024)
    
    def test_analyze_missing_end_year(self):
        """Test that analyze() raises error when end_year is missing."""
        with pytest.raises(ValueError, match="start_year and end_year are required"):
            analyze(latitude=28.6139, longitude=77.2090, start_year=2019, end_year=None)
    
    def test_analyze_latitude_below_boundary(self):
        """Test that analyze() rejects latitude below India's southern boundary."""
        with pytest.raises(ValueError, match="latitude must be between 6°N and 37°N"):
            analyze(latitude=5.0, longitude=77.2090, start_year=2019, end_year=2024)
    
    def test_analyze_latitude_above_boundary(self):
        """Test that analyze() rejects latitude above India's northern boundary."""
        with pytest.raises(ValueError, match="latitude must be between 6°N and 37°N"):
            analyze(latitude=38.0, longitude=77.2090, start_year=2019, end_year=2024)
    
    def test_analyze_longitude_below_boundary(self):
        """Test that analyze() rejects longitude below India's western boundary."""
        with pytest.raises(ValueError, match="longitude must be between 68°E and 97°E"):
            analyze(latitude=28.6139, longitude=67.0, start_year=2019, end_year=2024)
    
    def test_analyze_longitude_above_boundary(self):
        """Test that analyze() rejects longitude above India's eastern boundary."""
        with pytest.raises(ValueError, match="longitude must be between 68°E and 97°E"):
            analyze(latitude=28.6139, longitude=98.0, start_year=2019, end_year=2024)
    
    def test_analyze_invalid_year_range(self):
        """Test that analyze() rejects start_year > end_year."""
        with pytest.raises(ValueError, match="start_year .* cannot be after end_year"):
            analyze(latitude=28.6139, longitude=77.2090, start_year=2024, end_year=2019)
    
    def test_analyze_response_serializable(self):
        """Test that analyze() response can be serialized to JSON."""
        result = analyze(
            latitude=28.6139,
            longitude=77.2090,
            start_year=2019,
            end_year=2024
        )
        
        # Should not raise exception
        json_str = json.dumps(result)
        assert isinstance(json_str, str)
        
        # Should be deserializable
        deserialized = json.loads(json_str)
        assert deserialized == result
    
    def test_analyze_boundary_values(self):
        """Test analyze() with exact boundary coordinates."""
        # Test all four corners of India's boundaries
        corners = [
            (6, 68),    # Southwest
            (6, 97),    # Southeast
            (37, 68),   # Northwest
            (37, 97),   # Northeast
        ]
        
        for lat, lon in corners:
            result = analyze(latitude=lat, longitude=lon, start_year=2019, end_year=2024)
            assert "environmental_changes" in result
            assert "risk_forecast" in result
            assert "preventive_actions" in result


class TestChatService:
    """Tests for the mock chat service."""
    
    def test_chat_valid_input(self):
        """Test that chat() returns correct structure with valid inputs."""
        result = chat(
            query="What is the vegetation status?",
            state="Delhi",
            start_year=2019,
            end_year=2024
        )
        
        # Verify response structure
        assert "response" in result
        assert "context_used" in result
        
        # Verify field types
        assert isinstance(result["response"], str)
        assert isinstance(result["context_used"], bool)
        assert len(result["response"]) > 0
    
    def test_chat_missing_query(self):
        """Test that chat() raises error when query is missing."""
        with pytest.raises(ValueError, match="query is a required parameter"):
            chat(query=None, state="Delhi", start_year=2019, end_year=2024)
    
    def test_chat_empty_query(self):
        """Test that chat() raises error when query is empty."""
        with pytest.raises(ValueError, match="query is a required parameter and cannot be empty"):
            chat(query="", state="Delhi", start_year=2019, end_year=2024)
    
    def test_chat_missing_state(self):
        """Test that chat() raises error when state is missing."""
        with pytest.raises(ValueError, match="state is a required parameter"):
            chat(query="What is the status?", state=None, start_year=2019, end_year=2024)
    
    def test_chat_empty_state(self):
        """Test that chat() raises error when state is empty."""
        with pytest.raises(ValueError, match="state is a required parameter and cannot be empty"):
            chat(query="What is the status?", state="", start_year=2019, end_year=2024)
    
    def test_chat_missing_start_year(self):
        """Test that chat() raises error when start_year is missing."""
        with pytest.raises(ValueError, match="start_year is a required parameter"):
            chat(query="What is the status?", state="Delhi", start_year=None, end_year=2024)
    
    def test_chat_missing_end_year(self):
        """Test that chat() raises error when end_year is missing."""
        with pytest.raises(ValueError, match="end_year is a required parameter"):
            chat(query="What is the status?", state="Delhi", start_year=2019, end_year=None)
    
    def test_chat_invalid_year_range(self):
        """Test that chat() rejects start_year > end_year."""
        with pytest.raises(ValueError, match="start_year .* cannot be after end_year"):
            chat(query="What is the status?", state="Delhi", start_year=2024, end_year=2019)
    
    def test_chat_context_awareness(self):
        """Test that chat() incorporates context in responses."""
        result = chat(
            query="What is the vegetation status in this state?",
            state="Maharashtra",
            start_year=2020,
            end_year=2023
        )
        
        # Response should reference the state or time range
        response_lower = result["response"].lower()
        assert "maharashtra" in response_lower or "2020" in response_lower or "2023" in response_lower
        assert result["context_used"] is True
    
    def test_chat_response_serializable(self):
        """Test that chat() response can be serialized to JSON."""
        result = chat(
            query="What is the status?",
            state="Delhi",
            start_year=2019,
            end_year=2024
        )
        
        # Should not raise exception
        json_str = json.dumps(result)
        assert isinstance(json_str, str)
        
        # Should be deserializable
        deserialized = json.loads(json_str)
        assert deserialized == result
    
    def test_chat_different_query_types(self):
        """Test chat() with different types of queries."""
        queries = [
            "What is the vegetation status?",
            "Tell me about water resources",
            "How is urban development?",
            "What are the risks?",
            "Explain the climate patterns"
        ]
        
        for query in queries:
            result = chat(query=query, state="Delhi", start_year=2019, end_year=2024)
            assert "response" in result
            assert "context_used" in result
            assert len(result["response"]) > 0
