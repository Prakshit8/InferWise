"""
Example using the Context Manager.
"""

from inferwise.context import ContextManager

# Initialize context manager
context_manager = ContextManager(context_limit=2000)

# Create a conversation with duplicates and irrelevant messages
conversation = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there"},
    {"role": "user", "content": "Hello"},  # Duplicate
    {"role": "user", "content": "bye"},    # Irrelevant
    {"role": "user", "content": "Write a function to calculate fibonacci"},
    {"role": "assistant", "content": "Sure, here's a fibonacci function"},
]

# Process the context
response = context_manager.process(conversation)

print("=== Original Context ===")
print(f"Messages: {len(response.original_messages)}")
print(f"Tokens: {response.original_tokens}")

print("\n=== Processed Context ===")
print(f"Messages: {len(response.processed_messages)}")
print(f"Tokens: {response.processed_tokens}")

print("\n=== Processing Analytics ===")
print(f"Duplicates Removed: {response.duplicates_removed}")
print(f"Irrelevant Removed: {response.irrelevant_removed}")
print(f"Tokens Saved: {response.tokens_saved}")

print("\n=== Prioritization Scores ===")
for i, score in enumerate(response.prioritization_scores):
    print(f"Message {i}: {score:.3f}")

print("\n=== Processed Messages ===")
for msg in response.processed_messages:
    print(f"{msg['role']}: {msg['content'][:80]}...")
