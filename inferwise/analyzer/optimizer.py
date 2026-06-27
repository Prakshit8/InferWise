from typing import Dict, List


class OptimizationRecommender:
    """Recommend optimization strategies based on prompt analysis."""
    
    STRATEGIES = {
        "low_complexity": {
            "strategy": "minimal",
            "description": "Prompt is simple, minimal optimization needed",
            "actions": ["use_default_model", "enable_caching"],
        },
        "medium_complexity": {
            "strategy": "standard",
            "description": "Moderate complexity, apply standard optimizations",
            "actions": ["use_default_model", "enable_caching", "compress_context"],
        },
        "high_complexity": {
            "strategy": "aggressive",
            "description": "High complexity, apply all optimizations",
            "actions": [
                "use_larger_model",
                "enable_caching",
                "compress_context",
                "split_request",
                "use_temperature_tuning",
            ],
        },
        "coding_task": {
            "strategy": "code_optimized",
            "description": "Coding task detected, use code-specific optimizations",
            "actions": [
                "use_code_model",
                "enable_caching",
                "preserve_code_formatting",
            ],
        },
        "long_context": {
            "strategy": "context_optimized",
            "description": "Long context detected, optimize for token efficiency",
            "actions": [
                "compress_context",
                "use_summary",
                "enable_caching",
            ],
        },
    }
    
    def recommend(
        self,
        task: str,
        complexity: str,
        language: str = None,
        estimated_tokens: int = 0
    ) -> str:
        """Recommend optimization strategy.
        
        Args:
            task: Detected task category
            complexity: Complexity level
            language: Programming language (if any)
            estimated_tokens: Estimated token count
            
        Returns:
            Recommended optimization strategy
        """
        # Priority-based strategy selection
        if task == "coding":
            return self.STRATEGIES["coding_task"]["strategy"]
        
        if estimated_tokens > 2000:
            return self.STRATEGIES["long_context"]["strategy"]
        
        if complexity == "high":
            return self.STRATEGIES["high_complexity"]["strategy"]
        
        if complexity == "medium":
            return self.STRATEGIES["medium_complexity"]["strategy"]
        
        return self.STRATEGIES["low_complexity"]["strategy"]
    
    def get_strategy_details(self, strategy: str) -> Dict:
        """Get details about a strategy.
        
        Args:
            strategy: Strategy name
            
        Returns:
            Strategy details dictionary
        """
        for key, value in self.STRATEGIES.items():
            if value["strategy"] == strategy:
                return value
        return self.STRATEGIES["low_complexity"]
