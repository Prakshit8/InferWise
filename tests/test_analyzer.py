"""
Unit tests for Prompt Analyzer.
"""

import pytest
from inferwise.analyzer import PromptAnalyzer, AnalyzerResponse


def test_analyzer_initialization():
    """Test analyzer initialization."""
    analyzer = PromptAnalyzer()
    assert analyzer.task_detector is not None
    assert analyzer.language_detector is not None
    assert analyzer.complexity_estimator is not None
    assert analyzer.optimizer_recommender is not None


def test_analyze_coding_task():
    """Test analyzing a coding task."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "user", "content": "Write a function to calculate fibonacci numbers in Python"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.task == "coding"
    assert analysis.language == "python"
    assert analysis.complexity in ["low", "medium", "high"]
    assert analysis.estimated_tokens > 0
    assert analysis.recommended_provider == "groq"
    assert analysis.optimization_strategy in ["minimal", "standard", "aggressive", "code_optimized"]
    assert 0.0 <= analysis.confidence <= 1.0


def test_analyze_writing_task():
    """Test analyzing a writing task."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "user", "content": "Write an essay about climate change"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.task == "writing"
    assert analysis.language is None
    assert analysis.complexity in ["low", "medium", "high"]


def test_analyze_math_task():
    """Test analyzing a math task."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "user", "content": "Calculate 15 * 7 + 3"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.task == "math"
    assert analysis.complexity in ["low", "medium", "high"]


def test_analyze_general_task():
    """Test analyzing a general task."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "user", "content": "Tell me about yourself"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.task == "general"


def test_analyze_with_system_prompt():
    """Test analyzing with system prompt."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a Python function"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.metadata["has_system_prompt"] is True
    assert analysis.metadata["message_count"] == 2


def test_analyze_disabled():
    """Test analyzer when disabled."""
    analyzer = PromptAnalyzer()
    messages = [{"role": "user", "content": "Hello"}]
    
    analysis = analyzer.analyze(messages, enable_analysis=False)
    
    assert analysis is None


def test_analyze_javascript_code():
    """Test detecting JavaScript code."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "user", "content": "Write a function in JavaScript: function hello() { console.log('hi'); }"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.task == "coding"
    assert analysis.language == "javascript"


def test_analyze_high_complexity():
    """Test analyzing high complexity prompt."""
    analyzer = PromptAnalyzer()
    messages = [
        {
            "role": "user",
            "content": """
            Implement a distributed system for processing large-scale data using microservices architecture.
            The system should handle authentication, data encryption, and real-time processing.
            Also optimize for scalability and implement caching mechanisms.
            """
        }
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.complexity == "high"


def test_analyze_low_complexity():
    """Test analyzing low complexity prompt."""
    analyzer = PromptAnalyzer()
    messages = [
        {"role": "user", "content": "What is 2+2?"}
    ]
    
    analysis = analyzer.analyze(messages)
    
    assert analysis is not None
    assert analysis.complexity == "low"


def test_analyzer_response_to_dict():
    """Test converting AnalyzerResponse to dictionary."""
    response = AnalyzerResponse(
        task="coding",
        language="python",
        complexity="medium",
        estimated_tokens=100,
        recommended_provider="groq",
        optimization_strategy="code_optimized",
        confidence=0.8,
        metadata={"test": "value"}
    )
    
    response_dict = response.to_dict()
    
    assert response_dict["task"] == "coding"
    assert response_dict["language"] == "python"
    assert response_dict["complexity"] == "medium"
    assert response_dict["estimated_tokens"] == 100
    assert response_dict["recommended_provider"] == "groq"
    assert response_dict["optimization_strategy"] == "code_optimized"
    assert response_dict["confidence"] == 0.8
    assert response_dict["metadata"] == {"test": "value"}
