from typing import List, Dict, Any, Optional
from inferwise.context.response import ContextResponse
from inferwise.token_counter import count_messages


class ContextManager:
    """Manage conversation context by removing duplicates, irrelevant messages, and prioritizing relevant context."""
    
    def __init__(self, context_limit: int = 4000):
        """Initialize context manager.
        
        Args:
            context_limit: Maximum token limit for context (default: 4000)
        """
        self.context_limit = context_limit
    
    def process(
        self,
        messages: List[Dict[str, str]],
        enable_processing: bool = True
    ) -> ContextResponse:
        """Process conversation context.
        
        Args:
            messages: List of message dictionaries
            enable_processing: Whether to apply processing (default: True)
            
        Returns:
            ContextResponse with processing analytics
        """
        original_tokens = count_messages(messages)
        original_messages = [msg.copy() for msg in messages]
        
        if not enable_processing:
            return ContextResponse(
                original_messages=original_messages,
                processed_messages=original_messages,
                original_tokens=original_tokens,
                processed_tokens=original_tokens,
                tokens_saved=0,
                duplicates_removed=0,
                irrelevant_removed=0,
                prioritization_scores=[],
                metadata={"processing_disabled": True},
            )
        
        processed_messages = messages.copy()
        duplicates_removed = 0
        irrelevant_removed = 0
        
        # Remove duplicates
        processed_messages, duplicates_removed = self._remove_duplicates(processed_messages)
        
        # Remove irrelevant messages
        processed_messages, irrelevant_removed = self._remove_irrelevant(processed_messages)
        
        # Prioritize messages
        processed_messages, prioritization_scores = self._prioritize_messages(processed_messages)
        
        # Enforce context limit
        processed_messages = self._enforce_context_limit(processed_messages)
        
        processed_tokens = count_messages(processed_messages)
        tokens_saved = original_tokens - processed_tokens
        
        return ContextResponse(
            original_messages=original_messages,
            processed_messages=processed_messages,
            original_tokens=original_tokens,
            processed_tokens=processed_tokens,
            tokens_saved=tokens_saved,
            duplicates_removed=duplicates_removed,
            irrelevant_removed=irrelevant_removed,
            prioritization_scores=prioritization_scores,
            metadata={
                "messages_removed": len(original_messages) - len(processed_messages),
                "context_limit": self.context_limit,
            },
        )
    
    def _remove_duplicates(self, messages: List[Dict[str, str]]) -> tuple[List[Dict[str, str]], int]:
        """Remove duplicate messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Tuple of (deduplicated_messages, count_removed)
        """
        seen = set()
        deduplicated = []
        removed_count = 0
        
        for message in messages:
            # Create a hash of the message content and role
            message_key = (message.get("role", ""), message.get("content", "").strip())
            
            if message_key not in seen:
                seen.add(message_key)
                deduplicated.append(message)
            else:
                removed_count += 1
        
        return deduplicated, removed_count
    
    def _remove_irrelevant(self, messages: List[Dict[str, str]]) -> tuple[List[Dict[str, str]], int]:
        """Remove irrelevant messages (e.g., empty messages, greetings).
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Tuple of (filtered_messages, count_removed)
        """
        irrelevant_patterns = [
            "hi",
            "hello",
            "hey",
            "thanks",
            "thank you",
            "bye",
            "goodbye",
            "ok",
            "okay",
            "sure",
            "alright",
        ]
        
        filtered = []
        removed_count = 0
        
        for message in messages:
            content = message.get("content", "").strip().lower()
            
            # Skip empty messages
            if not content:
                removed_count += 1
                continue
            
            # Skip messages that are only greetings/thanks
            if content in irrelevant_patterns:
                removed_count += 1
                continue
            
            # Keep system messages always
            if message.get("role") == "system":
                filtered.append(message)
                continue
            
            filtered.append(message)
        
        return filtered, removed_count
    
    def _prioritize_messages(self, messages: List[Dict[str, str]]) -> tuple[List[Dict[str, str]], List[float]]:
        """Prioritize messages based on recency and semantic relevance.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Tuple of (prioritized_messages, scores)
        """
        if not messages:
            return messages, []
        
        # Calculate priority scores
        scores = []
        for i, message in enumerate(messages):
            score = 0.0
            
            # Recency bonus (more recent = higher score)
            score += (i / len(messages)) * 0.5
            
            # Role-based priority
            role = message.get("role", "")
            if role == "system":
                score += 0.5  # System messages are important
            elif role == "user":
                score += 0.3  # User messages are important
            elif role == "assistant":
                score += 0.2  # Assistant responses are less critical
            
            # Length-based priority (longer messages might be more important)
            content_length = len(message.get("content", ""))
            if content_length > 100:
                score += 0.1
            
            scores.append(score)
        
        # Sort messages by score (descending)
        indexed_messages = list(zip(messages, scores))
        indexed_messages.sort(key=lambda x: x[1], reverse=True)
        
        prioritized = [msg for msg, score in indexed_messages]
        sorted_scores = [score for msg, score in indexed_messages]
        
        return prioritized, sorted_scores
    
    def _enforce_context_limit(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Enforce context token limit by keeping highest-priority messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Messages within token limit
        """
        current_tokens = count_messages(messages)
        
        if current_tokens <= self.context_limit:
            return messages
        
        # Remove messages from the end until under limit
        # (assuming messages are already prioritized)
        result = messages.copy()
        
        while count_messages(result) > self.context_limit and len(result) > 1:
            # Remove lowest priority message (last in list)
            result.pop()
        
        return result
    
    def set_context_limit(self, limit: int) -> None:
        """Set the context token limit.
        
        Args:
            limit: New token limit
        """
        self.context_limit = limit
