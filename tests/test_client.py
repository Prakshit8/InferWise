"""
Unit tests for InferWise client.
"""

import pytest
from unittest.mock import Mock, patch
from inferwise import InferWise
from inferwise.response import Response


def test_client_initialization_with_provider():
    """Test client initialization with provider name."""
    with patch.dict('os.environ', {'GROQ_API_KEY': 'test_key'}):
        client = InferWise(provider="groq")
        assert client.provider_name == "groq"
        assert client.enable_logging is True


def test_client_initialization_with_api_key():
    """Test client initialization with explicit API key."""
    client = InferWise(provider="groq", api_key="test_key")
    assert client.provider_name == "groq"


def test_client_initialization_invalid_provider():
    """Test client initialization with invalid provider."""
    with pytest.raises(ValueError, match="Unsupported provider"):
        InferWise(provider="invalid")


def test_client_initialization_missing_api_key():
    """Test client initialization when API key is missing."""
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError, match="API key not found"):
            InferWise(provider="groq")


def test_client_disable_logging():
    """Test client with logging disabled."""
    with patch.dict('os.environ', {'GROQ_API_KEY': 'test_key'}):
        client = InferWise(provider="groq", enable_logging=False)
        assert client.enable_logging is False


def test_generate_with_mock():
    """Test generate method with mocked provider."""
    with patch.dict('os.environ', {'GROQ_API_KEY': 'test_key'}):
        client = InferWise(provider="groq", enable_logging=False)
        
        # Mock the provider's generate method
        mock_response = Response(
            content="Test response",
            model="llama-3.1-8b-instant",
            provider="groq",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            estimated_cost=0.000001,
            raw_response={}
        )
        client.provider.generate = Mock(return_value=mock_response)
        
        messages = [{"role": "user", "content": "Hello"}]
        response = client.generate(messages)
        
        assert response.content == "Test response"
        assert response.model == "llama-3.1-8b-instant"
        assert response.provider == "groq"
