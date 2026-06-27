from typing import Dict, Any, List
from groq import Groq
from inferwise.providers.base import BaseProvider
from inferwise.response import Response
from inferwise.token_counter import count_messages


class GroqProvider(BaseProvider):
    """Groq provider implementation."""
    
    # Cost per 1K tokens for Groq models (approximate)
    COST_PER_1K = {
        "llama-3.1-8b-instant": 0.00005,
        "llama-3.1-70b-instant": 0.00059,
        "llama-3.3-70b-versatile": 0.00059,
        "mixtral-8x7b-32768": 0.00027,
    }
    
    DEFAULT_MODEL = "llama-3.1-8b-instant"
    
    def __init__(self, api_key: str, model: str = None):
        super().__init__(api_key, model)
        self.model = model or self.DEFAULT_MODEL
        self.client = Groq(api_key=api_key)
    
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> Response:
        """Generate a response from Groq."""
        # Count prompt tokens
        prompt_tokens = self.count_tokens(messages)
        
        # Make API call
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        
        # Extract response data
        content = response.choices[0].message.content
        completion_tokens = response.usage.completion_tokens
        total_tokens = response.usage.total_tokens
        
        # Estimate cost
        estimated_cost = self.estimate_cost(prompt_tokens, completion_tokens)
        
        return Response(
            content=content,
            model=self.model,
            provider="groq",
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            estimated_cost=estimated_cost,
            raw_response={
                "id": response.id,
                "created": response.created,
                "model": response.model,
            }
        )
    
    def count_tokens(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens using tiktoken."""
        return count_messages(messages)
    
    def estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Estimate cost for the request."""
        cost_per_1k = self.COST_PER_1K.get(self.model, 0.00005)
        prompt_cost = (prompt_tokens / 1000) * cost_per_1k
        completion_cost = (completion_tokens / 1000) * cost_per_1k
        return prompt_cost + completion_cost
