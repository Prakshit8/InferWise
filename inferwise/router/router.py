from typing import Dict, Any, List, Optional, Callable
from inferwise.router.response import RoutingResponse
from inferwise.router.policy import (
    RoutingPolicy,
    CostOptimizedStrategy,
    LatencyOptimizedStrategy,
    QualityOptimizedStrategy,
    BalancedStrategy,
)


class ModelRouter:
    """Intelligent model router for selecting optimal provider."""
    
    # Provider capabilities (mock data - would be configurable in production)
    PROVIDER_CAPABILITIES = {
        "groq": {
            "cost_per_1k": 0.00005,
            "latency_ms": 50,
            "quality_score": 0.7,
            "context_limit": 8192,
        },
        "openai": {
            "cost_per_1k": 0.0005,
            "latency_ms": 500,
            "quality_score": 0.9,
            "context_limit": 128000,
        },
        "gemini": {
            "cost_per_1k": 0.000075,
            "latency_ms": 200,
            "quality_score": 0.85,
            "context_limit": 28000,
        },
    }
    
    # Strategy mapping
    STRATEGIES = {
        RoutingPolicy.COST_OPTIMIZED: CostOptimizedStrategy(),
        RoutingPolicy.LATENCY_OPTIMIZED: LatencyOptimizedStrategy(),
        RoutingPolicy.QUALITY_OPTIMIZED: QualityOptimizedStrategy(),
        RoutingPolicy.BALANCED: BalancedStrategy(),
    }
    
    def __init__(self, default_policy: RoutingPolicy = RoutingPolicy.BALANCED):
        """Initialize model router.
        
        Args:
            default_policy: Default routing policy (default: BALANCED)
        """
        self.default_policy = default_policy
        self.custom_policy: Optional[Callable] = None
    
    def route(
        self,
        task: str,
        complexity: str,
        context_size: int,
        policy: Optional[RoutingPolicy] = None,
        custom_policy: Optional[Callable] = None
    ) -> RoutingResponse:
        """Route to optimal provider based on criteria.
        
        Args:
            task: Task category
            complexity: Complexity level
            context_size: Context token size
            policy: Routing policy (uses default if None)
            custom_policy: Custom routing function
            
        Returns:
            RoutingResponse with selected provider and analytics
        """
        # Use custom policy if provided
        if custom_policy:
            selected_provider = custom_policy(task, complexity, context_size)
            return RoutingResponse(
                selected_provider=selected_provider,
                selected_model=self._get_default_model(selected_provider),
                routing_reason="custom_policy",
                scores={},
                metadata={"policy": "custom"},
            )
        
        # Use provided policy or default
        routing_policy = policy or self.default_policy
        strategy = self.STRATEGIES.get(routing_policy, self.STRATEGIES[RoutingPolicy.BALANCED])
        
        # Score each provider
        scores = {}
        for provider, capabilities in self.PROVIDER_CAPABILITIES.items():
            score = strategy.score(
                provider=provider,
                task=task,
                complexity=complexity,
                context_size=context_size,
                provider_capabilities=capabilities
            )
            scores[provider] = score
        
        # Select provider with highest score
        selected_provider = max(scores, key=scores.get)
        
        return RoutingResponse(
            selected_provider=selected_provider,
            selected_model=self._get_default_model(selected_provider),
            routing_reason=f"policy_{routing_policy.value}",
            scores=scores,
            metadata={
                "policy": routing_policy.value,
                "task": task,
                "complexity": complexity,
                "context_size": context_size,
            },
        )
    
    def _get_default_model(self, provider: str) -> str:
        """Get default model for provider.
        
        Args:
            provider: Provider name
            
        Returns:
            Default model name
        """
        models = {
            "groq": "llama-3.1-8b-instant",
            "openai": "gpt-4o-mini",
            "gemini": "gemini-1.5-flash",
        }
        return models.get(provider, "default")
    
    def set_custom_policy(self, policy: Callable) -> None:
        """Set a custom routing policy.
        
        Args:
            policy: Custom routing function
        """
        self.custom_policy = policy
    
    def update_provider_capabilities(self, provider: str, capabilities: Dict[str, Any]) -> None:
        """Update capabilities for a provider.
        
        Args:
            provider: Provider name
            capabilities: New capabilities
        """
        if provider in self.PROVIDER_CAPABILITIES:
            self.PROVIDER_CAPABILITIES[provider].update(capabilities)
