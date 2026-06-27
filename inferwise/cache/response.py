from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class CacheResponse:
    """Response from semantic cache lookup."""
    
    cache_hit: bool
    cached_response: Optional[str]
    similarity_score: float
    cache_latency_ms: float
    saved_cost: float
    saved_tokens: int
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "cache_hit": self.cache_hit,
            "cached_response": self.cached_response,
            "similarity_score": self.similarity_score,
            "cache_latency_ms": self.cache_latency_ms,
            "saved_cost": self.saved_cost,
            "saved_tokens": self.saved_tokens,
            "metadata": self.metadata,
        }
