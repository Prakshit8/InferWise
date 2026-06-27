from abc import ABC, abstractmethod
from typing import Dict, Any, List
from inferwise.response import Response


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, api_key: str, model: str = None):
        self.api_key = api_key
        self.model = model
    
    @abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> Response:
        """Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Response object with structured data
        """
        pass
    
    @abstractmethod
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Total token count
        """
        pass
    
    @abstractmethod
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost for the request.
        
        Args:
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            
        Returns:
            Estimated cost in USD
        """
        pass
