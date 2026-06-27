"""
Example using Conversation Memory.
"""

from inferwise.memory import ConversationMemory

# Initialize memory with a threshold
memory = ConversationMemory(token_threshold=1000)

# Create a long conversation history
long_conversation = [
    {"role": "system", "content": "You are a helpful coding assistant"},
    {"role": "user", "content": "My name is John and I work at Google"},
    {"role": "assistant", "content": "Hello John! How can I help you today?"},
    {"role": "user", "content": "I need to write a Python function"},
    {"role": "assistant", "content": "Sure, what kind of function do you need?"},
    {"role": "user", "content": "I prefer short and concise code"},
    {"role": "assistant", "content": "I'll keep that in mind"},
    {"role": "user", "content": "I still need to complete the data processing task"},
    {"role": "assistant", "content": "Let's work on that together"},
    {"role": "user", "content": "What is the best way to handle errors?"},
    {"role": "assistant", "content": "Try-except blocks are commonly used"},
]

# Compress the conversation
response = memory.compress(long_conversation)

print("=== Original Conversation ===")
print(f"Messages: {len(response.original_messages)}")
print(f"Tokens: {response.original_tokens}")

print("\n=== Compressed Conversation ===")
print(f"Messages: {len(response.compressed_messages)}")
print(f"Tokens: {response.compressed_tokens}")

print("\n=== Compression Analytics ===")
print(f"Tokens Saved: {response.tokens_saved}")
print(f"Percentage Saved: {response.percentage_saved:.2f}%")

print("\n=== Preserved Information ===")
print(f"Summary: {response.summary}")
print(f"Facts: {response.preserved_facts}")
print(f"Preferences: {response.preserved_preferences}")
print(f"Unfinished Tasks: {response.unfinished_tasks}")

print("\n=== Compressed Messages ===")
for msg in response.compressed_messages:
    print(f"{msg['role']}: {msg['content'][:100]}...")
