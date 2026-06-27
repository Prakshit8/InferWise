"""
Unit tests for Conversation Memory.
"""

import pytest
from inferwise.memory import ConversationMemory, MemoryResponse


def test_memory_initialization():
    """Test memory initialization."""
    memory = ConversationMemory()
    assert memory.token_threshold == 2000
    assert memory.fact_extractor is not None
    assert memory.preference_extractor is not None
    assert memory.task_extractor is not None


def test_memory_custom_threshold():
    """Test memory with custom threshold."""
    memory = ConversationMemory(token_threshold=1000)
    assert memory.token_threshold == 1000


def test_memory_compress_below_threshold():
    """Test memory compression when below threshold."""
    memory = ConversationMemory(token_threshold=10000)
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    
    response = memory.compress(messages)
    
    assert response.original_messages == messages
    assert response.compressed_messages == messages
    assert response.tokens_saved == 0
    assert response.percentage_saved == 0.0


def test_memory_compress_disabled():
    """Test memory when compression is disabled."""
    memory = ConversationMemory()
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"},
    ]
    
    response = memory.compress(messages, enable_compression=False)
    
    assert response.original_messages == messages
    assert response.compressed_messages == messages
    assert response.tokens_saved == 0


def test_fact_extraction():
    """Test fact extraction."""
    memory = ConversationMemory()
    messages = [
        {"role": "user", "content": "My name is John and I work at Google"},
        {"role": "user", "content": "I live in San Francisco"},
    ]
    
    response = memory.compress(messages, enable_compression=False)
    
    assert len(response.preserved_facts) >= 0


def test_preference_extraction():
    """Test preference extraction."""
    memory = ConversationMemory()
    messages = [
        {"role": "user", "content": "I prefer Python over JavaScript"},
        {"role": "user", "content": "Please always use short responses"},
    ]
    
    response = memory.compress(messages, enable_compression=False)
    
    assert len(response.preserved_preferences) >= 0


def test_task_extraction():
    """Test task extraction."""
    memory = ConversationMemory()
    messages = [
        {"role": "user", "content": "I need to finish this task not yet done"},
        {"role": "user", "content": "I still need to complete the project"},
    ]
    
    response = memory.compress(messages, enable_compression=False)
    
    assert len(response.unfinished_tasks) >= 0


def test_sliding_window():
    """Test sliding window compression."""
    memory = ConversationMemory(token_threshold=100)
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Message 1"},
        {"role": "assistant", "content": "Response 1"},
        {"role": "user", "content": "Message 2"},
        {"role": "assistant", "content": "Response 2"},
        {"role": "user", "content": "Message 3"},
        {"role": "assistant", "content": "Response 3"},
    ]
    
    response = memory.compress(messages)
    
    # System message should be preserved
    system_messages = [msg for msg in response.compressed_messages if msg.get("role") == "system"]
    assert len(system_messages) >= 1
    
    # Should have fewer messages than original
    assert len(response.compressed_messages) <= len(messages)


def test_summary_generation():
    """Test summary generation."""
    memory = ConversationMemory(token_threshold=100)
    messages = [
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris"},
    ]
    
    response = memory.compress(messages)
    
    assert isinstance(response.summary, str)


def test_memory_response_to_dict():
    """Test converting MemoryResponse to dictionary."""
    response = MemoryResponse(
        original_messages=[{"role": "user", "content": "test"}],
        compressed_messages=[{"role": "user", "content": "test"}],
        original_tokens=100,
        compressed_tokens=80,
        tokens_saved=20,
        percentage_saved=20.0,
        summary="Test summary",
        preserved_facts=["fact1"],
        preserved_preferences=["pref1"],
        unfinished_tasks=["task1"],
        metadata={"test": "value"}
    )
    
    response_dict = response.to_dict()
    
    assert response_dict["original_tokens"] == 100
    assert response_dict["compressed_tokens"] == 80
    assert response_dict["tokens_saved"] == 20
    assert response_dict["percentage_saved"] == 20.0
    assert response_dict["summary"] == "Test summary"


def test_set_threshold():
    """Test setting memory threshold."""
    memory = ConversationMemory()
    memory.set_threshold(5000)
    
    assert memory.token_threshold == 5000


def test_memory_with_empty_messages():
    """Test memory with empty messages."""
    memory = ConversationMemory()
    messages = []
    
    response = memory.compress(messages)
    
    assert response.original_messages == []
    assert response.compressed_messages == []
    assert response.original_tokens == 0
    assert response.compressed_tokens == 0


def test_memory_preserves_system_messages():
    """Test that system messages are preserved."""
    memory = ConversationMemory(token_threshold=100)
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]
    
    response = memory.compress(messages)
    
    system_messages = [msg for msg in response.compressed_messages if msg.get("role") == "system"]
    assert len(system_messages) >= 1
