from typing import List, Dict, Tuple
import re


class FactExtractor:
    """Extract important facts from conversation."""
    
    FACT_PATTERNS = [
        r"i\s+(?:am|was|have been)\s+(?:a|an|the)?\s*(\w+)",  # Identity
        r"my\s+(?:name|email|phone|address)\s+is\s+(.+)",  # Personal info
        r"i\s+(?:work|study)\s+(?:at|in)\s+(.+)",  # Work/study
        r"i\s+live\s+(?:in|at)\s+(.+)",  # Location
        r"i\s+(?:have|had)\s+(?:a|an)?\s*(.+)",  # Possessions
        r"the\s+(?:project|task|goal)\s+is\s+(.+)",  # Project info
    ]
    
    def extract(self, messages: List[Dict[str, str]]) -> List[str]:
        """Extract facts from messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of extracted facts
        """
        facts = []
        
        for message in messages:
            content = message.get("content", "").lower()
            for pattern in self.FACT_PATTERNS:
                matches = re.findall(pattern, content)
                for match in matches:
                    fact = match.strip()
                    if fact and len(fact) > 3:  # Filter short matches
                        facts.append(fact)
        
        # Deduplicate
        return list(set(facts))


class PreferenceExtractor:
    """Extract user preferences from conversation."""
    
    PREFERENCE_PATTERNS = [
        r"i\s+(?:prefer|like|love|enjoy)\s+(.+)",
        r"i\s+(?:don't|do not)\s+(?:like|prefer|want)\s+(.+)",
        r"please\s+(?:always|never)\s+(.+)",
        r"make\s+sure\s+to\s+(.+)",
        r"i\s+want\s+(.+)",
        r"i\s+need\s+(.+)",
    ]
    
    def extract(self, messages: List[Dict[str, str]]) -> List[str]:
        """Extract preferences from messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of extracted preferences
        """
        preferences = []
        
        for message in messages:
            content = message.get("content", "").lower()
            for pattern in self.PREFERENCE_PATTERNS:
                matches = re.findall(pattern, content)
                for match in matches:
                    pref = match.strip()
                    if pref and len(pref) > 3:
                        preferences.append(pref)
        
        return list(set(preferences))


class TaskExtractor:
    """Extract unfinished tasks from conversation."""
    
    TASK_PATTERNS = [
        r"i\s+need\s+to\s+(.+)",
        r"i\s+have\s+to\s+(.+)",
        r"i\s+should\s+(.+)",
        r"i\s+must\s+(.+)",
        r"help\s+me\s+(.+)",
        r"can\s+you\s+(?:help\s+me\s+)?(.+)",
        r"(?:we|let's)\s+need\s+to\s+(.+)",
    ]
    
    # Indicators that a task might be unfinished
    UNFINISHED_INDICATORS = [
        "not yet",
        "still need",
        "haven't",
        "waiting for",
        "to be done",
        "pending",
    ]
    
    def extract(self, messages: List[Dict[str, str]]) -> List[str]:
        """Extract unfinished tasks from messages.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            List of unfinished tasks
        """
        tasks = []
        
        for message in messages:
            content = message.get("content", "").lower()
            
            # Check if message contains unfinished indicators
            has_unfinished = any(indicator in content for indicator in self.UNFINISHED_INDICATORS)
            
            if has_unfinished:
                for pattern in self.TASK_PATTERNS:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        task = match.strip()
                        if task and len(task) > 3:
                            tasks.append(task)
        
        return list(set(tasks))
