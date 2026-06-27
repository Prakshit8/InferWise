from typing import List, Dict, Any, Optional
from inferwise.optimizer.strategies import BaseStrategy, WhitespaceRemoval, RedundancyRemoval, ConstraintMerging
from inferwise.optimizer.response import OptimizationResponse
from inferwise.token_counter import count_tokens


class PromptOptimizer:
    """Optimize prompts using a pipeline of strategies."""
    
    def __init__(self, strategies: Optional[List[BaseStrategy]] = None):
        """Initialize optimizer with strategies.
        
        Args:
            strategies: List of optimization strategies (default: all strategies)
        """
        self.strategies = strategies or [
            WhitespaceRemoval(),
            RedundancyRemoval(),
            ConstraintMerging(),
        ]
    
    def optimize(
        self,
        text: str,
        enable_optimization: bool = True
    ) -> OptimizationResponse:
        """Optimize a single prompt.
        
        Args:
            text: The text to optimize
            enable_optimization: Whether to apply optimization (default: True)
            
        Returns:
            OptimizationResponse with analytics
        """
        original_tokens = count_tokens([{"content": text}])
        original_text = text
        
        if not enable_optimization:
            return OptimizationResponse(
                original_text=original_text,
                optimized_text=original_text,
                original_tokens=original_tokens,
                optimized_tokens=original_tokens,
                tokens_saved=0,
                percentage_saved=0.0,
                strategies_applied=[],
                metadata={"optimization_disabled": True},
            )
        
        optimized_text = text
        strategies_applied = []
        all_metadata = {}
        
        # Apply strategies in pipeline
        for strategy in self.strategies:
            try:
                before = optimized_text
                optimized_text, metadata = strategy.optimize(optimized_text)
                after = optimized_text
                
                if before != after:
                    strategies_applied.append(strategy.name)
                    all_metadata[strategy.name] = metadata
            except Exception as e:
                # Log error but continue with other strategies
                all_metadata[f"{strategy.name}_error"] = str(e)
        
        optimized_tokens = count_tokens([{"content": optimized_text}])
        tokens_saved = original_tokens - optimized_tokens
        percentage_saved = (tokens_saved / original_tokens * 100) if original_tokens > 0 else 0.0
        
        return OptimizationResponse(
            original_text=original_text,
            optimized_text=optimized_text,
            original_tokens=original_tokens,
            optimized_tokens=optimized_tokens,
            tokens_saved=tokens_saved,
            percentage_saved=percentage_saved,
            strategies_applied=strategies_applied,
            metadata=all_metadata,
        )
    
    def add_strategy(self, strategy: BaseStrategy) -> None:
        """Add a strategy to the pipeline.
        
        Args:
            strategy: Strategy to add
        """
        self.strategies.append(strategy)
    
    def remove_strategy(self, strategy_name: str) -> bool:
        """Remove a strategy from the pipeline.
        
        Args:
            strategy_name: Name of strategy to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, strategy in enumerate(self.strategies):
            if strategy.name == strategy_name:
                self.strategies.pop(i)
                return True
        return False
