from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class ContextResponse:
    """Response from context management."""
    
    original_messages: List[Dict[str, str]]
    processed_messages: List[Dict[str, str]]
    original_tokens: int
    processed_tokens: int
    tokens_saved: int
    duplicates_removed: int
    irrelevant_removed: int
    prioritization_scores: List[float]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "original_messages": self.original_messages,
            "processed_messages": self.processed_messages,
            "original_tokens": self.original_tokens,
            "processed_tokens": self.processed_tokens,
            "tokens_saved": self.tokens_saved,
            "duplicates_removed": self.duplicates_removed,
            "irrelevant_removed": self.irrelevant_removed,
            "prioritization_scores": self.prioritization_scores,
            "metadata": self.metadata,
        }
