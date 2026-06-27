from typing import Dict
import re


class ComplexityEstimator:
    """Estimate complexity of a prompt."""
    
    def __init__(self):
        self.complexity_weights = {
            "length": 0.3,
            "code_blocks": 0.4,
            "technical_terms": 0.2,
            "nested_requests": 0.1,
        }
    
    def estimate(self, text: str, task: str, language: str = None) -> str:
        """Estimate complexity of the prompt.
        
        Args:
            text: The prompt text
            task: Detected task category
            language: Detected programming language (if any)
            
        Returns:
            Complexity level: "low", "medium", or "high"
        """
        scores = {
            "length": self._score_length(text),
            "code_blocks": self._score_code_blocks(text),
            "technical_terms": self._score_technical_terms(text, task),
            "nested_requests": self._score_nested_requests(text),
        }
        
        # Calculate weighted score
        total_score = sum(
            scores[key] * self.complexity_weights[key]
            for key in scores
        )
        
        # Map to complexity levels
        if total_score < 0.3:
            return "low"
        elif total_score < 0.7:
            return "medium"
        else:
            return "high"
    
    def _score_length(self, text: str) -> float:
        """Score based on text length."""
        length = len(text)
        if length < 100:
            return 0.0
        elif length < 300:
            return 0.3
        elif length < 500:
            return 0.6
        else:
            return 1.0
    
    def _score_code_blocks(self, text: str) -> float:
        """Score based on number of code blocks."""
        # Count code blocks (triple backticks)
        code_blocks = text.count("```")
        # Count inline code (single backticks)
        inline_code = text.count("`") - (code_blocks * 3)
        
        code_score = min((code_blocks / 2) + (inline_code / 10), 1.0)
        return code_score
    
    def _score_technical_terms(self, text: str, task: str) -> float:
        """Score based on technical term density."""
        technical_terms = [
            "algorithm", "data structure", "complexity", "optimization",
            "asynchronous", "concurrent", "parallel", "distributed",
            "authentication", "authorization", "encryption", "security",
            "database", "api", "rest", "graphql", "websocket",
            "machine learning", "neural network", "deep learning",
            "recursion", "iteration", "polymorphism", "inheritance",
            "design pattern", "architecture", "scalability",
        ]
        
        text_lower = text.lower()
        term_count = sum(1 for term in technical_terms if term in text_lower)
        
        # Adjust based on task
        if task == "coding":
            return min(term_count / 5, 1.0)
        elif task == "analysis":
            return min(term_count / 3, 1.0)
        else:
            return min(term_count / 8, 1.0)
    
    def _score_nested_requests(self, text: str) -> float:
        """Score based on nested or compound requests."""
        nested_indicators = [
            r"and\s+then",
            r"after\s+that",
            r"also\s+(?:please|can\s+you)",
            r"in\s+addition",
            r"furthermore",
            r"moreover",
            r"besides",
            r"first.*then.*finally",
            r"not\s+only.*but\s+also",
        ]
        
        text_lower = text.lower()
        nested_count = sum(
            1 for pattern in nested_indicators
            if re.search(pattern, text_lower)
        )
        
        return min(nested_count / 3, 1.0)
