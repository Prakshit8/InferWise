from typing import List, Dict, Any, Optional
from inferwise.memory.extractor import FactExtractor, PreferenceExtractor, TaskExtractor
from inferwise.memory.response import MemoryResponse
from inferwise.token_counter import count_messages


class ConversationMemory:
    """Manage conversation history with sliding-window memory compression."""
    
    def __init__(self, token_threshold: int = 2000):
        """Initialize conversation memory.
        
        Args:
            token_threshold: Token count threshold for compression (default: 2000)
        """
        self.token_threshold = token_threshold
        self.fact_extractor = FactExtractor()
        self.preference_extractor = PreferenceExtractor()
        self.task_extractor = TaskExtractor()
    
    def compress(
        self,
        messages: List[Dict[str, str]],
        enable_compression: bool = True
    ) -> MemoryResponse:
        """Compress conversation history if it exceeds threshold.
        
        Args:
            messages: List of message dictionaries
            enable_compression: Whether to apply compression (default: True)
            
        Returns:
            MemoryResponse with compression analytics
        """
        original_tokens = count_messages(messages)
        original_messages = [msg.copy() for msg in messages]
        
        if not enable_compression or original_tokens <= self.token_threshold:
            return MemoryResponse(
                original_messages=original_messages,
                compressed_messages=original_messages,
                original_tokens=original_tokens,
                compressed_tokens=original_tokens,
                tokens_saved=0,
                percentage_saved=0.0,
                summary="",
                preserved_facts=[],
                preserved_preferences=[],
                unfinished_tasks=[],
                metadata={"compression_disabled": True or original_tokens <= self.token_threshold},
            )
        
        # Extract important information before compression
        preserved_facts = self.fact_extractor.extract(messages)
        preserved_preferences = self.preference_extractor.extract(messages)
        unfinished_tasks = self.task_extractor.extract(messages)
        
        # Generate summary of old messages
        summary = self._generate_summary(messages)
        
        # Compress messages using sliding window
        compressed_messages = self._apply_sliding_window(messages)
        
        # Insert summary as a system message at the beginning
        if summary:
            compressed_messages.insert(0, {
                "role": "system",
                "content": f"Conversation summary: {summary}"
            })
        
        compressed_tokens = count_messages(compressed_messages)
        tokens_saved = original_tokens - compressed_tokens
        percentage_saved = (tokens_saved / original_tokens * 100) if original_tokens > 0 else 0.0
        
        return MemoryResponse(
            original_messages=original_messages,
            compressed_messages=compressed_messages,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            tokens_saved=tokens_saved,
            percentage_saved=percentage_saved,
            summary=summary,
            preserved_facts=preserved_facts,
            preserved_preferences=preserved_preferences,
            unfinished_tasks=unfinished_tasks,
            metadata={
                "messages_removed": len(original_messages) - len(compressed_messages),
                "threshold_exceeded": original_tokens > self.token_threshold,
            },
        )
    
    def _generate_summary(self, messages: List[Dict[str, str]]) -> str:
        """Generate a summary of the conversation.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Summary string
        """
        if not messages:
            return ""
        
        # Extract key points from messages
        key_points = []
        
        for message in messages:
            content = message.get("content", "")
            role = message.get("role", "")
            
            # Extract first sentence from each message
            sentences = content.split('.')
            if sentences:
                first_sentence = sentences[0].strip()
                if first_sentence:
                    key_points.append(f"{role}: {first_sentence}")
        
        # Limit summary to key points
        summary_points = key_points[:5]  # Keep top 5 points
        return ". ".join(summary_points) + "."
    
    def _apply_sliding_window(self, messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Apply sliding window to keep recent messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Compressed list of messages
        """
        # Keep system messages and recent user/assistant messages
        system_messages = [msg for msg in messages if msg.get("role") == "system"]
        other_messages = [msg for msg in messages if msg.get("role") != "system"]
        
        # Keep last N messages based on token threshold
        # Rough estimate: keep last 10-15 messages for typical threshold
        window_size = max(5, len(other_messages) // 2)  # Keep at least half
        
        recent_messages = other_messages[-window_size:]
        
        return system_messages + recent_messages
    
    def set_threshold(self, threshold: int) -> None:
        """Set the token threshold for compression.
        
        Args:
            threshold: New token threshold
        """
        self.token_threshold = threshold
