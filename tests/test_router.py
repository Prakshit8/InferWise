"""
Unit tests for Model Router.
"""

import pytest
from inferwise.router import ModelRouter, RoutingResponse, RoutingPolicy


def test_router_initialization():
    """Test router initialization."""
    router = ModelRouter()
    assert router.default_policy == RoutingPolicy.BALANCED


def test_router_custom_policy():
    """Test router with custom policy."""
    router = ModelRouter(default_policy=RoutingPolicy.COST_OPTIMIZED)
    assert router.default_policy == RoutingPolicy.COST_OPTIMIZED


def test_route_cost_optimized():
    """Test cost-optimized routing."""
    router = ModelRouter(default_policy=RoutingPolicy.COST_OPTIMIZED)
    
    response = router.route(
        task="coding",
        complexity="low",
        context_size=1000
    )
    
    assert response.selected_provider in ["groq", "openai", "gemini"]
    assert "cost" in response.routing_reason


def test_route_latency_optimized():
    """Test latency-optimized routing."""
    router = ModelRouter(default_policy=RoutingPolicy.LATENCY_OPTIMIZED)
    
    response = router.route(
        task="coding",
        complexity="low",
        context_size=1000
    )
    
    assert response.selected_provider in ["groq", "openai", "gemini"]
    assert "latency" in response.routing_reason


def test_route_quality_optimized():
    """Test quality-optimized routing."""
    router = ModelRouter(default_policy=RoutingPolicy.QUALITY_OPTIMIZED)
    
    response = router.route(
        task="coding",
        complexity="high",
        context_size=5000
    )
    
    assert response.selected_provider in ["groq", "openai", "gemini"]
    assert "quality" in response.routing_reason


def test_route_balanced():
    """Test balanced routing."""
    router = ModelRouter(default_policy=RoutingPolicy.BALANCED)
    
    response = router.route(
        task="coding",
        complexity="medium",
        context_size=2000
    )
    
    assert response.selected_provider in ["groq", "openai", "gemini"]
    assert len(response.scores) == 3


def test_custom_routing_policy():
    """Test custom routing policy."""
    router = ModelRouter()
    
    def custom_policy(task, complexity, context_size):
        return "groq"  # Always route to Groq
    
    response = router.route(
        task="coding",
        complexity="high",
        context_size=1000,
        custom_policy=custom_policy
    )
    
    assert response.selected_provider == "groq"
    assert response.routing_reason == "custom_policy"


def test_routing_response_to_dict():
    """Test converting RoutingResponse to dictionary."""
    response = RoutingResponse(
        selected_provider="groq",
        selected_model="llama-3.1-8b-instant",
        routing_reason="test",
        scores={"groq": 0.9, "openai": 0.7},
        metadata={"test": "value"}
    )
    
    response_dict = response.to_dict()
    
    assert response_dict["selected_provider"] == "groq"
    assert response_dict["selected_model"] == "llama-3.1-8b-instant"
    assert response_dict["routing_reason"] == "test"
    assert response_dict["scores"] == {"groq": 0.9, "openai": 0.7}


def test_set_custom_policy():
    """Test setting custom policy."""
    router = ModelRouter()
    
    def custom_policy(task, complexity, context_size):
        return "openai"
    
    router.set_custom_policy(custom_policy)
    
    assert router.custom_policy is not None


def test_update_provider_capabilities():
    """Test updating provider capabilities."""
    router = ModelRouter()
    
    router.update_provider_capabilities("groq", {"latency_ms": 30})
    
    assert router.PROVIDER_CAPABILITIES["groq"]["latency_ms"] == 30


def test_route_with_high_complexity():
    """Test routing with high complexity (should prefer quality)."""
    router = ModelRouter(default_policy=RoutingPolicy.QUALITY_OPTIMIZED)
    
    response = router.route(
        task="coding",
        complexity="high",
        context_size=3000
    )
    
    # High complexity should favor providers with better quality
    assert response.selected_provider in ["groq", "openai", "gemini"]


def test_route_with_large_context():
    """Test routing with large context size."""
    router = ModelRouter(default_policy=RoutingPolicy.QUALITY_OPTIMIZED)
    
    response = router.route(
        task="analysis",
        complexity="medium",
        context_size=10000
    )
    
    # Large context should favor providers with higher context limits
    assert response.selected_provider in ["groq", "openai", "gemini"]
