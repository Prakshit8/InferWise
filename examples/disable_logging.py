"""
Example with logging disabled.
"""

from inferwise import InferWise

# Initialize client with logging disabled
client = InferWise(
    provider="groq",
    enable_logging=False
)

messages = [
    {"role": "user", "content": "What is 2+2?"},
]

response = client.generate(messages)

print(f"Response: {response.content}")
print(f"Tokens: {response.total_tokens}")
