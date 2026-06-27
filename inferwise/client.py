import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
from inferwise.providers.groq import GroqProvider
from inferwise.providers.openai import OpenAIProvider
from inferwise.providers.gemini import GeminiProvider
from inferwise.response import Response
from inferwise.logger import log_request
from inferwise.analyzer import PromptAnalyzer, AnalyzerResponse
from inferwise.optimizer import PromptOptimizer, OptimizationResponse
from inferwise.memory import ConversationMemory, MemoryResponse
from inferwise.context import ContextManager, ContextResponse
from inferwise.router import ModelRouter, RoutingResponse, RoutingPolicy

load_dotenv()


class InferWise:
    """Main client for InferWise SDK."""
    
    SUPPORTED_PROVIDERS = {
        "groq": GroqProvider,
        "openai": OpenAIProvider,
        "gemini": GeminiProvider,
    }
    
    def __init__(
        self,
        provider: str = "groq",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        enable_logging: bool = True,
        enable_analysis: bool = True,
        enable_optimization: bool = True,
        memory_threshold: int = 2000,
        context_limit: int = 4000,
        enable_routing: bool = False,
        routing_policy: Optional[RoutingPolicy] = None,
    ):
        """Initialize InferWise client.
        
        Args:
            provider: Name of the provider (default: "groq")
            api_key: API key (if None, loads from environment variable)
            model: Model name (provider-specific)
            enable_logging: Whether to log requests (default: True)
            enable_analysis: Whether to enable prompt analysis (default: True)
            enable_optimization: Whether to enable prompt optimization (default: True)
            memory_threshold: Token threshold for conversation memory compression (default: 2000)
            context_limit: Token limit for context management (default: 4000)
            enable_routing: Whether to enable intelligent routing (default: False)
            routing_policy: Routing policy to use (default: BALANCED)
        """
        if provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Supported providers: {list(self.SUPPORTED_PROVIDERS.keys())}"
            )
        
        self.provider_name = provider
        self.enable_logging = enable_logging
        self.enable_analysis = enable_analysis
        self.enable_optimization = enable_optimization
        self.memory_threshold = memory_threshold
        self.context_limit = context_limit
        self.enable_routing = enable_routing
        self.routing_policy = routing_policy or RoutingPolicy.BALANCED
        
        # Initialize analyzer, optimizer, memory, context manager, and router
        self.analyzer = PromptAnalyzer()
        self.optimizer = PromptOptimizer()
        self.memory = ConversationMemory(token_threshold=memory_threshold)
        self.context_manager = ContextManager(context_limit=context_limit)
        self.router = ModelRouter(default_policy=self.routing_policy)
        
        # Load API key from environment if not provided
        if api_key is None:
            env_key = f"{provider.upper()}_API_KEY"
            api_key = os.getenv(env_key)
            if not api_key:
                raise ValueError(
                    f"API key not found. Please provide api_key or set {env_key} environment variable."
                )
        
        # Initialize provider
        provider_class = self.SUPPORTED_PROVIDERS[provider]
        self.provider = provider_class(api_key=api_key, model=model)
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        **kwargs
    ) -> Response:
        """Generate a response from the LLM.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Response object with structured data
        """
        # Process context (remove duplicates, irrelevant, prioritize)
        context_processing: Optional[ContextResponse] = None
        context_processing = self.context_manager.process(messages, enable_processing=True)
        messages = context_processing.processed_messages
        
        # Compress conversation history if it exceeds threshold
        memory_compression: Optional[MemoryResponse] = None
        if len(messages) > 1:  # Only compress if there's a conversation
            memory_compression = self.memory.compress(messages, enable_compression=True)
            messages = memory_compression.compressed_messages
        
        # Analyze prompt if enabled
        analysis: Optional[AnalyzerResponse] = None
        if self.enable_analysis:
            analysis = self.analyzer.analyze(messages, enable_analysis=True)
        
        # Route to optimal provider if enabled
        routing: Optional[RoutingResponse] = None
        if self.enable_routing and analysis:
            routing = self.router.route(
                task=analysis.task,
                complexity=analysis.complexity,
                context_size=context_processing.processed_tokens,
            )
            # Note: In a full implementation, we would switch providers here
            # For now, we just log the routing decision
        
        # Optimize the last user message if enabled
        optimization: Optional[OptimizationResponse] = None
        if self.enable_optimization:
            # Find the last user message
            for i in range(len(messages) - 1, -1, -1):
                if messages[i].get("role") == "user":
                    original_content = messages[i]["content"]
                    optimization = self.optimizer.optimize(original_content, enable_optimization=True)
                    messages[i]["content"] = optimization.optimized_text
                    break
        
        # Generate response through provider
        response = self.provider.generate(messages, **kwargs)
        
        # Log request if enabled
        if self.enable_logging:
            log_data = {
                "timestamp": str(response.raw_response.get("created", "")),
                "provider": response.provider,
                "model": response.model,
                "prompt_tokens": response.prompt_tokens,
                "completion_tokens": response.completion_tokens,
                "total_tokens": response.total_tokens,
                "estimated_cost": response.estimated_cost,
                "messages": messages,
            }
            
            # Add analysis data if available
            if analysis:
                log_data["analysis"] = analysis.to_dict()
            
            # Add optimization data if available
            if optimization:
                log_data["optimization"] = optimization.to_dict()
            
            # Add memory compression data if available
            if memory_compression:
                log_data["memory_compression"] = memory_compression.to_dict()
            
            # Add context processing data if available
            if context_processing:
                log_data["context_processing"] = context_processing.to_dict()
            
            # Add routing data if available
            if routing:
                log_data["routing"] = routing.to_dict()
            
            log_request(log_data)
        
        return response