"""
Unit tests for Groq provider.
"""

import pytest
from unittest.mock import Mock, patch
from inferwise.providers.groq import GroqProvider


def test_groq_provider_initialization():
    """Test Groq provider initialization."""
    provider = GroqProvider(api_key="test_key")
    assert provider.api_key == "test_key"
    assert provider.model == "llama-3.1-8b-instant"


def test_groq_provider_custom_model():
    """Test Groq provider with custom model."""
    provider = GroqProvider(api_key="test_key", model="llama-3.1-70b-instant")
    assert provider.model == "llama-3.1-70b-instant"


def test_groq_count_tokens():
    """Test token counting in Groq provider."""
    provider = GroqProvider(api_key="test_key")
    messages = [{"role": "user", "content": "Hello"}]
    tokens = provider.count_tokens(messages)
    assert tokens > 0


def test_groq_estimate_cost():
    """Test cost estimation in Groq provider."""
    provider = GroqProvider(api_key="test_key")
    cost = provider.estimate_cost(1000, 500)
    assert cost > 0
    assert isinstance(cost, float)


def test_groq_estimate_cost_zero():
    """Test cost estimation with zero tokens."""
    provider = GroqProvider(api_key="test_key")
    cost = provider.estimate_cost(0, 0)
    assert cost == 0.0
