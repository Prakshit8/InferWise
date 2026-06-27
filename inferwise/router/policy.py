from abc import ABC, abstractmethod
from typing import Dict, Any, List
from enum import Enum


class RoutingPolicy(Enum):
    """Routing policy types."""
    COST_OPTIMIZED = "cost_optimized"
    LATENCY_OPTIMIZED = "latency_optimized"
    QUALITY_OPTIMIZED = "quality_optimized"
    BALANCED = "balanced"


class BaseRoutingStrategy(ABC):
    """Base class for routing strategies."""
    
    def __init__(self):
        self.name = self.__class__.__name__
    
    @abstractmethod
    def score(
        self,
        provider: str,
        task: str,
        complexity: str,
        context_size: int,
        provider_capabilities: Dict[str, Any]
    ) -> float:
        """Calculate routing score for a provider.
        
        Args:
            provider: Provider name
            task: Task category
            complexity: Complexity level
            context_size: Context token size
            provider_capabilities: Provider capabilities dict
            
        Returns:
            Routing score (higher is better)
        """
        pass


class CostOptimizedStrategy(BaseRoutingStrategy):
    """Routing strategy optimized for cost."""
    
    def score(
        self,
        provider: str,
        task: str,
        complexity: str,
        context_size: int,
        provider_capabilities: Dict[str, Any]
    ) -> float:
        """Score based on cost efficiency."""
        cost_per_1k = provider_capabilities.get("cost_per_1k", 0.001)
        
        # Lower cost = higher score
        base_score = 1.0 / (cost_per_1k * 1000 + 0.001)
        
        # Adjust for complexity - simple tasks can use cheaper models
        if complexity == "low":
            base_score *= 1.2
        elif complexity == "high":
            base_score *= 0.8
        
        return base_score


class LatencyOptimizedStrategy(BaseRoutingStrategy):
    """Routing strategy optimized for latency."""
    
    def score(
        self,
        provider: str,
        task: str,
        complexity: str,
        context_size: int,
        provider_capabilities: Dict[str, Any]
    ) -> float:
        """Score based on latency."""
        latency_ms = provider_capabilities.get("latency_ms", 100)
        
        # Lower latency = higher score
        base_score = 1.0 / (latency_ms + 1)
        
        # Adjust for context size
        if context_size > 2000:
            base_score *= 0.7  # Penalize for large context
        
        return base_score


class QualityOptimizedStrategy(BaseRoutingStrategy):
    """Routing strategy optimized for quality."""
    
    def score(
        self,
        provider: str,
        task: str,
        complexity: str,
        context_size: int,
        provider_capabilities: Dict[str, Any]
    ) -> float:
        """Score based on quality/capability."""
        quality_score = provider_capabilities.get("quality_score", 0.5)
        context_limit = provider_capabilities.get("context_limit", 4096)
        
        base_score = quality_score
        
        # Prefer providers with higher context limits for complex tasks
        if complexity == "high" and context_limit > 8000:
            base_score *= 1.3
        
        # Adjust for context size
        if context_size > context_limit * 0.8:
            base_score *= 0.5  # Penalize if near limit
        
        return base_score


class BalancedStrategy(BaseRoutingStrategy):
    """Balanced routing strategy considering all factors."""
    
    def score(
        self,
        provider: str,
        task: str,
        complexity: str,
        context_size: int,
        provider_capabilities: Dict[str, Any]
    ) -> float:
        """Score based on balanced approach."""
        cost_score = 1.0 / (provider_capabilities.get("cost_per_1k", 0.001) * 1000 + 0.001)
        latency_score = 1.0 / (provider_capabilities.get("latency_ms", 100) + 1)
        quality_score = provider_capabilities.get("quality_score", 0.5)
        
        # Weighted average
        base_score = (cost_score * 0.3 + latency_score * 0.3 + quality_score * 0.4)
        
        # Adjust for complexity
        if complexity == "high":
            base_score *= 1.1  # Prefer quality for complex tasks
        elif complexity == "low":
            base_score *= 1.1  # Prefer cost for simple tasks
        
        return base_score
