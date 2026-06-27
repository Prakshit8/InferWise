"""
Example using a custom model with InferWise SDK.
"""

from inferwise import InferWise

# Initialize client with a specific model
client = InferWise(
    provider="groq",
    model="llama-3.1-70b-instant"
)

messages = [
    {"role": "user", "content": "Explain quantum computing in simple terms."},
]

response = client.generate(messages)

print(f"Response: {response.content}")
print(f"Model Used: {response.model}")
print(f"Cost: ${response.estimated_cost:.6f}")
