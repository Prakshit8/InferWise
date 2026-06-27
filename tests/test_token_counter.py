"""
Unit tests for token counter.
"""

from inferwise.token_counter import count_tokens, count_messages


def test_count_tokens():
    """Test counting tokens in a string."""
    text = "Hello, world!"
    tokens = count_tokens(text)
    assert tokens > 0
    assert isinstance(tokens, int)


def test_count_tokens_empty():
    """Test counting tokens in an empty string."""
    tokens = count_tokens("")
    assert tokens == 0


def test_count_messages():
    """Test counting tokens in messages."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ]
    tokens = count_messages(messages)
    assert tokens > 0
    assert isinstance(tokens, int)


def test_count_messages_empty():
    """Test counting tokens in empty messages."""
    messages = []
    tokens = count_messages(messages)
    assert tokens == 0


def test_count_messages_single():
    """Test counting tokens in a single message."""
    messages = [
        {"role": "user", "content": "Test message"},
    ]
    tokens = count_messages(messages)
    assert tokens > 0
