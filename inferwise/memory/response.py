from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class MemoryResponse:
    """Response from conversation memory compression."""
    
    original_messages: List[Dict[str, str]]
    compressed_messages: List[Dict[str, str]]
    original_tokens: int
    compressed_tokens: int
    tokens_saved: int
    percentage_saved: float
    summary: str
    preserved_facts: List[str]
    preserved_preferences: List[str]
    unfinished_tasks: List[str]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "original_messages": self.original_messages,
            "compressed_messages": self.compressed_messages,
            "original_tokens": self.original_tokens,
            "compressed_tokens": self.compressed_tokens,
            "tokens_saved": self.tokens_saved,
            "percentage_saved": self.percentage_saved,
            "summary": self.summary,
            "preserved_facts": self.preserved_facts,
            "preserved_preferences": self.preserved_preferences,
            "unfinished_tasks": self.unfinished_tasks,
            "metadata": self.metadata,
        }
