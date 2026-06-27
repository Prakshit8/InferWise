import tiktoken
from typing import List, Dict

ENCODING = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str) -> int:
    """Count tokens in a string.
    
    Args:
        text: The text to count tokens for
        
    Returns:
        Number of tokens
    """
    return len(ENCODING.encode(text))


def count_messages(messages: List[Dict[str, str]]) -> int:
    """Count tokens in a list of messages.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        
    Returns:
        Total token count across all messages
    """
    total_tokens = 0
    for message in messages:
        total_tokens += count_tokens(message["content"])
    return total_tokens