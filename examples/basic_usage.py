"""
Basic usage example for InferWise SDK.
"""

from inferwise import InferWise

# Initialize client (loads GROQ_API_KEY from .env)
client = InferWise(provider="groq")

# Create messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"},
]

# Generate response
response = client.generate(messages)

# Print response
print(f"Content: {response.content}")
print(f"Model: {response.model}")
print(f"Provider: {response.provider}")
print(f"Prompt Tokens: {response.prompt_tokens}")
print(f"Completion Tokens: {response.completion_tokens}")
print(f"Total Tokens: {response.total_tokens}")
print(f"Estimated Cost: ${response.estimated_cost:.6f}")
