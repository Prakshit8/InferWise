"""
Unit tests for Context Manager.
"""

import pytest
from inferwise.context import ContextManager, ContextResponse


def test_context_manager_initialization():
    """Test context manager initialization."""
    manager = ContextManager()
    assert manager.context_limit == 4000


def test_context_manager_custom_limit():
    """Test context manager with custom limit."""
    manager = ContextManager(context_limit=2000)
    assert manager.context_limit == 2000


def test_remove_duplicates():
    """Test duplicate removal."""
    manager = ContextManager()
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi"},
    ]
    
    response = manager.process(messages, enable_processing=True)
    
    assert response.duplicates_removed == 1
    assert len(response.processed_messages) == 2


def test_remove_irrelevant():
    """Test irrelevant message removal."""
    manager = ContextManager()
    messages = [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "hi"},
        {"role": "user", "content": "bye"},
        {"role": "user", "content": "Actual question here"},
    ]
    
    response = manager.process(messages, enable_processing=True)
    
    assert response.irrelevant_removed >= 2


def test_prioritize_messages():
    """Test message prioritization."""
    manager = ContextManager()
    messages = [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "Question"},
        {"role": "assistant", "content": "Answer"},
    ]
    
    response = manager.process(messages, enable_processing=True)
    
    assert len(response.prioritization_scores) == 3
    # System message should have highest score
    assert max(response.prioritization_scores) > 0


def test_context_limit_enforcement():
    """Test context limit enforcement."""
    manager = ContextManager(context_limit=10)
    messages = [
        {"role": "user", "content": "This is a very long message " * 100},
        {"role": "assistant", "content": "Response " * 100},
    ]
    
    response = manager.process(messages, enable_processing=True)
    
    assert response.processed_tokens <= manager.context_limit


def test_context_processing_disabled():
    """Test context processing when disabled."""
    manager = ContextManager()
    messages = [
        {"role": "user", "content": "Hello"},
        {"role": "user", "content": "Hello"},
    ]
    
    response = manager.process(messages, enable_processing=False)
    
    assert response.processed_messages == messages
    assert response.duplicates_removed == 0


def test_context_response_to_dict():
    """Test converting ContextResponse to dictionary."""
    response = ContextResponse(
        original_messages=[{"role": "user", "content": "test"}],
        processed_messages=[{"role": "user", "content": "test"}],
        original_tokens=100,
        processed_tokens=80,
        tokens_saved=20,
        duplicates_removed=1,
        irrelevant_removed=2,
        prioritization_scores=[0.5, 0.3],
        metadata={"test": "value"}
    )
    
    response_dict = response.to_dict()
    
    assert response_dict["original_tokens"] == 100
    assert response_dict["processed_tokens"] == 80
    assert response_dict["tokens_saved"] == 20
    assert response_dict["duplicates_removed"] == 1
    assert response_dict["irrelevant_removed"] == 2


def test_set_context_limit():
    """Test setting context limit."""
    manager = ContextManager()
    manager.set_context_limit(5000)
    
    assert manager.context_limit == 5000


def test_context_with_empty_messages():
    """Test context manager with empty messages."""
    manager = ContextManager()
    messages = []
    
    response = manager.process(messages)
    
    assert response.original_messages == []
    assert response.processed_messages == []
    assert response.original_tokens == 0


def test_context_preserves_system_messages():
    """Test that system messages are preserved."""
    manager = ContextManager()
    messages = [
        {"role": "system", "content": "You are helpful"},
        {"role": "user", "content": "hi"},
    ]
    
    response = manager.process(messages)
    
    system_messages = [msg for msg in response.processed_messages if msg.get("role") == "system"]
    assert len(system_messages) == 1


def test_context_with_empty_content():
    """Test handling of messages with empty content."""
    manager = ContextManager()
    messages = [
        {"role": "user", "content": ""},
        {"role": "user", "content": "   "},
        {"role": "user", "content": "Actual message"},
    ]
    
    response = manager.process(messages)
    
    # Empty messages should be removed
    assert len(response.processed_messages) == 1
