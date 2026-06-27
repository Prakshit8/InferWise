from typing import List, Dict, Optional
from inferwise.analyzer.detector import TaskDetector, LanguageDetector
from inferwise.analyzer.complexity import ComplexityEstimator
from inferwise.analyzer.optimizer import OptimizationRecommender
from inferwise.analyzer.response import AnalyzerResponse
from inferwise.token_counter import count_messages


class PromptAnalyzer:
    """Analyze prompts to extract metadata and recommendations."""
    
    def __init__(self):
        self.task_detector = TaskDetector()
        self.language_detector = LanguageDetector()
        self.complexity_estimator = ComplexityEstimator()
        self.optimizer_recommender = OptimizationRecommender()
    
    def analyze(
        self,
        messages: List[Dict[str, str]],
        enable_analysis: bool = True
    ) -> Optional[AnalyzerResponse]:
        """Analyze prompt messages.
        
        Args:
            messages: List of message dictionaries
            enable_analysis: Whether to perform analysis (default: True)
            
        Returns:
            AnalyzerResponse with analysis results, or None if disabled
        """
        if not enable_analysis:
            return None
        
        # Extract text from messages (focus on last user message)
        text = self._extract_text(messages)
        
        # Detect task and language
        task = self.task_detector.detect(text)
        language = self.language_detector.detect(text)
        
        # Estimate complexity
        complexity = self.complexity_estimator.estimate(text, task, language)
        
        # Estimate tokens
        estimated_tokens = count_messages(messages)
        
        # Recommend optimization strategy
        optimization_strategy = self.optimizer_recommender.recommend(
            task=task,
            complexity=complexity,
            language=language,
            estimated_tokens=estimated_tokens
        )
        
        # Recommend provider based on task and complexity
        recommended_provider = self._recommend_provider(task, complexity, language)
        
        # Calculate confidence
        confidence = self._calculate_confidence(task, language, complexity)
        
        # Build metadata
        metadata = {
            "message_count": len(messages),
            "has_system_prompt": any(msg.get("role") == "system" for msg in messages),
            "last_role": messages[-1].get("role") if messages else None,
        }
        
        return AnalyzerResponse(
            task=task,
            language=language,
            complexity=complexity,
            estimated_tokens=estimated_tokens,
            recommended_provider=recommended_provider,
            optimization_strategy=optimization_strategy,
            confidence=confidence,
            metadata=metadata,
        )
    
    def _extract_text(self, messages: List[Dict[str, str]]) -> str:
        """Extract text from messages for analysis.
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            Combined text from messages
        """
        # Focus on the last user message for analysis
        for msg in reversed(messages):
            if msg.get("role") == "user":
                return msg.get("content", "")
        
        # Fallback to last message
        if messages:
            return messages[-1].get("content", "")
        
        return ""
    
    def _recommend_provider(
        self,
        task: str,
        complexity: str,
        language: Optional[str]
    ) -> str:
        """Recommend provider based on analysis.
        
        Args:
            task: Detected task
            complexity: Complexity level
            language: Programming language
            
        Returns:
            Recommended provider name
        """
        # For Phase 1, only Groq is available
        # In future phases, this would recommend based on task/complexity
        return "groq"
    
    def _calculate_confidence(
        self,
        task: str,
        language: Optional[str],
        complexity: str
    ) -> float:
        """Calculate confidence score for analysis.
        
        Args:
            task: Detected task
            language: Detected language
            complexity: Complexity level
            
        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.5  # Base confidence
        
        # Increase confidence if task is not "general"
        if task != "general":
            confidence += 0.2
        
        # Increase confidence if language was detected
        if language:
            confidence += 0.2
        
        # Increase confidence for clear complexity levels
        if complexity in ["low", "high"]:
            confidence += 0.1
        
        return min(confidence, 1.0)
