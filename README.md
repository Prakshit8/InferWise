# InferWise

InferWise is an AI Middleware SDK that provides a unified interface for interacting with multiple LLM providers. Phase 1 supports Groq with a clean, modular architecture designed for extensibility.

## Features

- **Provider Abstraction**: Clean interface for adding new LLM providers
- **Structured Responses**: Returns typed Response objects instead of raw API responses
- **Token Counting**: Built-in token counting using tiktoken
- **Request Logging**: Automatic logging of requests to JSON files
- **Cost Estimation**: Real-time cost estimation for API calls
- **Type Hints**: Full type annotations for better IDE support
- **Environment Configuration**: Load API keys from .env files
- **Prompt Analyzer**: Analyze prompts to detect task type, programming language, complexity, and recommend optimization strategies
- **Prompt Optimization**: Compress prompts by removing redundancy, whitespace, and merging constraints while preserving meaning
- **Conversation Memory**: Sliding-window memory compression with fact, preference, and task preservation
- **Context Manager**: Remove duplicates, irrelevant messages, and prioritize context based on relevance
- **Intelligent Routing**: Automatically select optimal provider based on task, cost, latency, and complexity

## Installation

```bash
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

1. Create a `.env` file in your project root:

```env
GROQ_API_KEY=your_api_key_here
```

2. Use InferWise in your code:

```python
from inferwise import InferWise

client = InferWise(provider="groq")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

response = client.generate(messages)

print(response.content)
```

## Usage

### Basic Usage

```python
from inferwise import InferWise

client = InferWise(provider="groq")

messages = [
    {"role": "user", "content": "Explain quantum computing."},
]

response = client.generate(messages)
print(f"Response: {response.content}")
print(f"Tokens: {response.total_tokens}")
print(f"Cost: ${response.estimated_cost:.6f}")
```

### Custom Model

```python
client = InferWise(
    provider="groq",
    model="llama-3.1-70b-instant"
)
```

### Disable Logging

```python
client = InferWise(
    provider="groq",
    enable_logging=False
)
```

### Multi-turn Conversations

```python
client = InferWise(provider="groq")

conversation = [
    {"role": "system", "content": "You are a helpful tutor."},
    {"role": "user", "content": "What is 15 * 7?"},
]

response1 = client.generate(conversation)
conversation.append({"role": "assistant", "content": response1.content})
conversation.append({"role": "user", "content": "Now what is 15 * 8?"})

response2 = client.generate(conversation)
```

### Using the Prompt Analyzer

The Prompt Analyzer automatically analyzes your prompts to detect task type, programming language, complexity, and recommend optimization strategies.

```python
from inferwise import InferWise
from inferwise.analyzer import PromptAnalyzer

# Use analyzer standalone
analyzer = PromptAnalyzer()
messages = [
    {"role": "user", "content": "Write a function to calculate fibonacci in Python"}
]

analysis = analyzer.analyze(messages)
print(f"Task: {analysis.task}")  # "coding"
print(f"Language: {analysis.language}")  # "python"
print(f"Complexity: {analysis.complexity}")  # "low", "medium", or "high"
print(f"Optimization Strategy: {analysis.optimization_strategy}")
```

The analyzer is automatically integrated into `InferWise.generate()`:

```python
client = InferWise(provider="groq", enable_analysis=True)

response = client.generate(messages)
# Analysis is automatically performed and logged
```

To disable analysis:

```python
client = InferWise(provider="groq", enable_analysis=False)
```

### Using Prompt Optimization

Prompt Optimization automatically compresses prompts by removing redundancy, whitespace, and merging constraints while preserving meaning.

```python
from inferwise.optimizer import PromptOptimizer

optimizer = PromptOptimizer()

verbose_prompt = "Please can you please write a function for me? Make it fast and efficient."

response = optimizer.optimize(verbose_prompt)

print(f"Original: {response.original_text}")
print(f"Optimized: {response.optimized_text}")
print(f"Tokens Saved: {response.tokens_saved}")
print(f"Percentage Saved: {response.percentage_saved:.2f}%")
```

The optimizer is automatically integrated into `InferWise.generate()`:

```python
client = InferWise(provider="groq", enable_optimization=True)

response = client.generate(messages)
# The last user message is automatically optimized
```

To disable optimization:

```python
client = InferWise(provider="groq", enable_optimization=False)
```

### Using Conversation Memory

Conversation Memory automatically compresses long conversation histories using a sliding-window approach while preserving important facts, preferences, and unfinished tasks.

```python
from inferwise.memory import ConversationMemory

memory = ConversationMemory(token_threshold=2000)

# Long conversation history
long_conversation = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "My name is John"},
    {"role": "assistant", "content": "Hello John!"},
    # ... many more messages
]

response = memory.compress(long_conversation)

print(f"Original Tokens: {response.original_tokens}")
print(f"Compressed Tokens: {response.compressed_tokens}")
print(f"Tokens Saved: {response.tokens_saved}")
print(f"Preserved Facts: {response.preserved_facts}")
print(f"Preserved Preferences: {response.preserved_preferences}")
print(f"Unfinished Tasks: {response.unfinished_tasks}")
```

The memory engine is automatically integrated into `InferWise.generate()`:

```python
client = InferWise(provider="groq", memory_threshold=2000)

response = client.generate(messages)
# Conversation is automatically compressed if it exceeds threshold
```

To adjust the memory threshold:

```python
client = InferWise(provider="groq", memory_threshold=5000)
```

### Using Context Manager

Context Manager automatically processes conversation context by removing duplicates, irrelevant messages, and prioritizing relevant context.

```python
from inferwise.context import ContextManager

context_manager = ContextManager(context_limit=2000)

conversation = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"},
    {"role": "user", "content": "Hello"},  # Duplicate
    {"role": "user", "content": "bye"},    # Irrelevant
    {"role": "user", "content": "Actual question"},
]

response = context_manager.process(conversation)

print(f"Duplicates Removed: {response.duplicates_removed}")
print(f"Irrelevant Removed: {response.irrelevant_removed}")
print(f"Tokens Saved: {response.tokens_saved}")
```

The context manager is automatically integrated into `InferWise.generate()`:

```python
client = InferWise(provider="groq", context_limit=4000)

response = client.generate(messages)
# Context is automatically processed before generation
```

To adjust the context limit:

```python
client = InferWise(provider="groq", context_limit=8000)
```

### Using Intelligent Model Routing

Model Router automatically selects the optimal provider based on task, cost, latency, and complexity.

```python
from inferwise.router import ModelRouter, RoutingPolicy

router = ModelRouter(default_policy=RoutingPolicy.BALANCED)

response = router.route(
    task="coding",
    complexity="high",
    context_size=3000
)

print(f"Selected Provider: {response.selected_provider}")
print(f"Selected Model: {response.selected_model}")
print(f"Scores: {response.scores}")
```

Available routing policies:
- **COST_OPTIMIZED**: Prioritizes lowest cost
- **LATENCY_OPTIMIZED**: Prioritizes fastest response
- **QUALITY_OPTIMIZED**: Prioritizes highest quality
- **BALANCED**: Considers all factors equally

Custom routing policies:

```python
def custom_policy(task, complexity, context_size):
    if task == "coding":
        return "groq"
    return "openai"

router.set_custom_policy(custom_policy)
```

The router is automatically integrated into `InferWise.generate()`:

```python
from inferwise.router import RoutingPolicy

client = InferWise(
    provider="groq",
    enable_routing=True,
    routing_policy=RoutingPolicy.COST_OPTIMIZED
)

response = client.generate(messages)
# Router automatically selects optimal provider
```

## Response Object

The `Response` object provides structured data:

```python
@dataclass
class Response:
    content: str              # Generated text
    model: str                # Model used
    provider: str             # Provider name
    prompt_tokens: int        # Input token count
    completion_tokens: int   # Output token count
    total_tokens: int        # Total token count
    estimated_cost: float     # Estimated cost in USD
    raw_response: Optional[Dict]  # Raw API response
```

## Analyzer Response Object

The `AnalyzerResponse` object provides prompt analysis data:

```python
@dataclass
class AnalyzerResponse:
    task: str                      # Detected task (coding, writing, analysis, math, general)
    language: Optional[str]        # Detected programming language
    complexity: str               # Complexity level (low, medium, high)
    estimated_tokens: int         # Estimated token count
    recommended_provider: str     # Recommended provider
    optimization_strategy: str    # Recommended optimization strategy
    confidence: float             # Analysis confidence score (0.0 - 1.0)
    metadata: Dict[str, Any]      # Additional metadata
```

### Detected Task Categories

- **coding**: Code generation, debugging, refactoring
- **writing**: Essay, article, content creation
- **analysis**: Data analysis, explanation, comparison
- **math**: Mathematical calculations and problem-solving
- **general**: General queries and conversations

### Detected Programming Languages

Python, JavaScript, Java, C, C++, Go, Rust, SQL, HTML, CSS

### Optimization Strategies

- **minimal**: Simple prompts, minimal optimization needed
- **standard**: Moderate complexity, standard optimizations
- **aggressive**: High complexity, all optimizations applied
- **code_optimized**: Coding tasks with code-specific optimizations
- **context_optimized**: Long context, token efficiency optimizations

## Optimization Response Object

The `OptimizationResponse` object provides prompt optimization analytics:

```python
@dataclass
class OptimizationResponse:
    original_text: str              # Original prompt text
    optimized_text: str             # Optimized prompt text
    original_tokens: int           # Original token count
    optimized_tokens: int          # Optimized token count
    tokens_saved: int              # Number of tokens saved
    percentage_saved: float        # Percentage of tokens saved
    strategies_applied: list[str]  # List of applied strategies
    metadata: Dict[str, Any]       # Strategy-specific metadata
```

### Optimization Strategies

- **WhitespaceRemoval**: Removes excessive whitespace and blank lines
- **RedundancyRemoval**: Removes redundant phrases and instructions
- **ConstraintMerging**: Merges repeated constraints and instructions

## Memory Response Object

The `MemoryResponse` object provides conversation memory compression analytics:

```python
@dataclass
class MemoryResponse:
    original_messages: List[Dict]      # Original message list
    compressed_messages: List[Dict]    # Compressed message list
    original_tokens: int               # Original token count
    compressed_tokens: int             # Compressed token count
    tokens_saved: int                 # Number of tokens saved
    percentage_saved: float            # Percentage of tokens saved
    summary: str                      # Conversation summary
    preserved_facts: List[str]        # Extracted facts
    preserved_preferences: List[str]  # Extracted preferences
    unfinished_tasks: List[str]       # Unfinished tasks
    metadata: Dict[str, Any]          # Additional metadata
```

## Context Response Object

The `ContextResponse` object provides context processing analytics:

```python
@dataclass
class ContextResponse:
    original_messages: List[Dict]      # Original message list
    processed_messages: List[Dict]    # Processed message list
    original_tokens: int               # Original token count
    processed_tokens: int             # Processed token count
    tokens_saved: int                 # Number of tokens saved
    duplicates_removed: int           # Number of duplicates removed
    irrelevant_removed: int           # Number of irrelevant messages removed
    prioritization_scores: List[float] # Priority scores for messages
    metadata: Dict[str, Any]          # Additional metadata
```

## Routing Response Object

The `RoutingResponse` object provides model routing analytics:

```python
@dataclass
class RoutingResponse:
    selected_provider: str             # Selected provider name
    selected_model: str                # Selected model name
    routing_reason: str               # Reason for routing decision
    scores: Dict[str, float]          # Provider scores
    metadata: Dict[str, Any]          # Additional metadata
```

## Supported Providers

- **Groq** (Phase 1)
  - Models: llama-3.1-8b-instant, llama-3.1-70b-instant, llama-3.3-70b-versatile, mixtral-8x7b-32768
- **OpenAI** (Phase 6)
  - Models: gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo
- **Gemini** (Phase 6)
  - Models: gemini-1.5-pro, gemini-1.5-flash, gemini-1.0-pro

## Examples

See the `examples/` directory for more usage examples:

- `basic_usage.py` - Basic usage example
- `custom_model.py` - Using custom models
- `disable_logging.py` - Disabling logging
- `conversation.py` - Multi-turn conversations
- `prompt_analyzer.py` - Using the Prompt Analyzer
- `prompt_optimizer.py` - Using the Prompt Optimizer
- `conversation_memory.py` - Using Conversation Memory
- `context_manager.py` - Using the Context Manager
- `model_router.py` - Using the Model Router

## Testing

Run the test suite:

```bash
pytest tests/
```

Run with coverage:

```bash
pytest tests/ --cov=inferwise
```

## Project Structure

```
inferwise/
├── inferwise/
│   ├── __init__.py
│   ├── client.py           # Main InferWise client
│   ├── response.py        # Response dataclass
│   ├── logger.py          # Request logging
│   ├── token_counter.py   # Token counting with tiktoken
│   ├── analyzer/          # Prompt Analyzer (Phase 2)
│   │   ├── __init__.py
│   │   ├── analyzer.py    # Main analyzer
│   │   ├── detector.py    # Task and language detection
│   │   ├── complexity.py  # Complexity estimation
│   │   ├── optimizer.py   # Optimization strategy recommendation
│   │   └── response.py    # Analyzer response dataclass
│   ├── optimizer/         # Prompt Optimizer (Phase 3)
│   │   ├── __init__.py
│   │   ├── optimizer.py   # Main optimizer with pipeline
│   │   ├── strategies.py  # Pluggable optimization strategies
│   │   └── response.py    # Optimization response dataclass
│   ├── memory/            # Conversation Memory (Phase 4)
│   │   ├── __init__.py
│   │   ├── memory.py      # Main memory engine
│   │   ├── extractor.py   # Fact/preference/task extractors
│   │   └── response.py    # Memory response dataclass
│   ├── context/           # Context Manager (Phase 5)
│   │   ├── __init__.py
│   │   ├── context.py     # Main context manager
│   │   └── response.py    # Context response dataclass
│   ├── router/            # Model Router (Phase 6)
│   │   ├── __init__.py
│   │   ├── router.py      # Main router with policies
│   │   ├── policy.py      # Routing strategies
│   │   └── response.py    # Routing response dataclass
│   └── providers/
│       ├── __init__.py
│       ├── base.py        # Provider abstraction
│       ├── groq.py        # Groq provider implementation
│       ├── openai.py      # OpenAI provider implementation
│       └── gemini.py      # Gemini provider implementation
├── examples/              # Usage examples
├── tests/                 # Unit tests
├── pyproject.toml        # Project configuration
└── README.md
```

## License

MIT

## Roadmap

- [ ] Phase 2: Add OpenAI provider
- [ ] Phase 2: Add Anthropic provider
- [ ] Phase 3: Add response caching
- [ ] Phase 3: Add rate limiting
- [ ] Phase 4: Add automatic retry logic
- [ ] Phase 4: Add streaming responses
