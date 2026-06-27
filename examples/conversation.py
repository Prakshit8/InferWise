"""
Example of a multi-turn conversation.
"""

from inferwise import InferWise

client = InferWise(provider="groq")

# Start a conversation
conversation = [
    {"role": "system", "content": "You are a helpful math tutor."},
    {"role": "user", "content": "What is 15 * 7?"},
]

# First response
response1 = client.generate(conversation)
print(f"Assistant: {response1.content}")

# Add assistant's response to conversation
conversation.append({"role": "assistant", "content": response1.content})

# Ask follow-up question
conversation.append({"role": "user", "content": "Now what is 15 * 8?"})

# Second response
response2 = client.generate(conversation)
print(f"Assistant: {response2.content}")
