from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class OptimizationResponse:
    """Response from prompt optimization."""
    
    original_text: str
    optimized_text: str
    original_tokens: int
    optimized_tokens: int
    tokens_saved: int
    percentage_saved: float
    strategies_applied: list[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "original_text": self.original_text,
            "optimized_text": self.optimized_text,
            "original_tokens": self.original_tokens,
            "optimized_tokens": self.optimized_tokens,
            "tokens_saved": self.tokens_saved,
            "percentage_saved": self.percentage_saved,
            "strategies_applied": self.strategies_applied,
            "metadata": self.metadata,
        }
