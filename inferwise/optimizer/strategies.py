from abc import ABC, abstractmethod
from typing import Dict, Any
import re


class BaseStrategy(ABC):
    """Base class for optimization strategies."""
    
    def __init__(self):
        self.name = self.__class__.__name__
    
    @abstractmethod
    def optimize(self, text: str) -> tuple[str, Dict[str, Any]]:
        """Apply optimization strategy to text.
        
        Args:
            text: The text to optimize
            
        Returns:
            Tuple of (optimized_text, metadata)
        """
        pass


class WhitespaceRemoval(BaseStrategy):
    """Remove unnecessary whitespace while preserving structure."""
    
    def optimize(self, text: str) -> tuple[str, Dict[str, Any]]:
        """Remove excessive whitespace."""
        # Remove leading/trailing whitespace from each line
        lines = text.split('\n')
        stripped_lines = [line.strip() for line in lines]
        
        # Remove multiple consecutive blank lines
        optimized_lines = []
        blank_count = 0
        for line in stripped_lines:
            if line == '':
                blank_count += 1
                if blank_count <= 1:  # Keep single blank lines
                    optimized_lines.append(line)
            else:
                blank_count = 0
                optimized_lines.append(line)
        
        optimized_text = '\n'.join(optimized_lines)
        
        # Remove multiple spaces within lines
        optimized_text = re.sub(r' +', ' ', optimized_text)
        
        metadata = {
            "original_lines": len(lines),
            "optimized_lines": len(optimized_lines),
            "blank_lines_removed": len(lines) - len(optimized_lines),
        }
        
        return optimized_text, metadata


class RedundancyRemoval(BaseStrategy):
    """Remove redundant instructions and phrases."""
    
    REDUNDANT_PHRASES = [
        r"please\s+",
        r"can\s+you\s+please\s+",
        r"i\s+would\s+like\s+you\s+to\s+",
        r"i\s+need\s+you\s+to\s+",
        r"kindly\s+",
        r"if\s+you\s+could\s+",
        r"it\s+would\s+be\s+great\s+if\s+you\s+could\s+",
        r"i\s+want\s+you\s+to\s+",
        r"make\s+sure\s+to\s+",
        r"don't\s+forget\s+to\s+",
        r"remember\s+to\s+",
    ]
    
    def optimize(self, text: str) -> tuple[str, Dict[str, Any]]:
        """Remove redundant phrases."""
        optimized_text = text.lower()
        
        removed_phrases = []
        for pattern in self.REDUNDANT_PHRASES:
            matches = re.findall(pattern, optimized_text)
            if matches:
                removed_phrases.extend(matches)
                optimized_text = re.sub(pattern, '', optimized_text)
        
        # Clean up resulting double spaces
        optimized_text = re.sub(r' +', ' ', optimized_text)
        optimized_text = optimized_text.strip()
        
        # Capitalize first letter
        if optimized_text:
            optimized_text = optimized_text[0].upper() + optimized_text[1:]
        
        metadata = {
            "phrases_removed": len(removed_phrases),
            "removed_phrases": removed_phrases[:5],  # Limit to first 5
        }
        
        return optimized_text, metadata


class ConstraintMerging(BaseStrategy):
    """Merge repeated constraints and instructions."""
    
    def optimize(self, text: str) -> tuple[str, Dict[str, Any]]:
        """Merge repeated constraints."""
        # Extract sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Find similar sentences (simple similarity based on common words)
        unique_sentences = []
        merged_count = 0
        
        for sentence in sentences:
            is_duplicate = False
            words = set(sentence.lower().split())
            
            for existing in unique_sentences:
                existing_words = set(existing.lower().split())
                # If sentences share 70%+ of words, consider them duplicates
                if words and existing_words:
                    overlap = len(words & existing_words)
                    similarity = overlap / max(len(words), len(existing_words))
                    if similarity > 0.7:
                        is_duplicate = True
                        merged_count += 1
                        break
            
            if not is_duplicate:
                unique_sentences.append(sentence)
        
        optimized_text = '. '.join(unique_sentences)
        if optimized_text and not optimized_text.endswith('.'):
            optimized_text += '.'
        
        metadata = {
            "original_sentences": len(sentences),
            "optimized_sentences": len(unique_sentences),
            "sentences_merged": merged_count,
        }
        
        return optimized_text, metadata
