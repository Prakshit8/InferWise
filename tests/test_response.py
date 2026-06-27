"""
Unit tests for Response object.
"""

from inferwise.response import Response


def test_response_creation():
    """Test creating a Response object."""
    response = Response(
        content="Test content",
        model="test-model",
        provider="test-provider",
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
        estimated_cost=0.0001
    )
    
    assert response.content == "Test content"
    assert response.model == "test-model"
    assert response.provider == "test-provider"
    assert response.prompt_tokens == 10
    assert response.completion_tokens == 5
    assert response.total_tokens == 15
    assert response.estimated_cost == 0.0001
    assert response.raw_response is None


def test_response_with_raw_response():
    """Test creating a Response object with raw response."""
    raw = {"id": "test-id", "created": 123456}
    response = Response(
        content="Test content",
        model="test-model",
        provider="test-provider",
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
        estimated_cost=0.0001,
        raw_response=raw
    )
    
    assert response.raw_response == raw


def test_response_to_dict():
    """Test converting Response to dictionary."""
    response = Response(
        content="Test content",
        model="test-model",
        provider="test-provider",
        prompt_tokens=10,
        completion_tokens=5,
        total_tokens=15,
        estimated_cost=0.0001
    )
    
    response_dict = response.to_dict()
    
    assert response_dict["content"] == "Test content"
    assert response_dict["model"] == "test-model"
    assert response_dict["provider"] == "test-provider"
    assert response_dict["prompt_tokens"] == 10
    assert response_dict["completion_tokens"] == 5
    assert response_dict["total_tokens"] == 15
    assert response_dict["estimated_cost"] == 0.0001
