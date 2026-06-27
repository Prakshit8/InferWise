from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class AnalyzerResponse:
    """Structured response from prompt analyzer."""
    
    task: str
    language: Optional[str]
    complexity: str
    estimated_tokens: int
    recommended_provider: str
    optimization_strategy: str
    confidence: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "task": self.task,
            "language": self.language,
            "complexity": self.complexity,
            "estimated_tokens": self.estimated_tokens,
            "recommended_provider": self.recommended_provider,
            "optimization_strategy": self.optimization_strategy,
            "confidence": self.confidence,
            "metadata": self.metadata,
        }
