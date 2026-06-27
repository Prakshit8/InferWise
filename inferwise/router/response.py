from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class RoutingResponse:
    """Response from model routing."""
    
    selected_provider: str
    selected_model: str
    routing_reason: str
    scores: Dict[str, float]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "selected_provider": self.selected_provider,
            "selected_model": self.selected_model,
            "routing_reason": self.routing_reason,
            "scores": self.scores,
            "metadata": self.metadata,
        }
