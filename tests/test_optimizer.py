"""
Unit tests for Prompt Optimizer.
"""

import pytest
from inferwise.optimizer import PromptOptimizer, OptimizationResponse
from inferwise.optimizer.strategies import WhitespaceRemoval, RedundancyRemoval, ConstraintMerging


def test_optimizer_initialization():
    """Test optimizer initialization."""
    optimizer = PromptOptimizer()
    assert len(optimizer.strategies) == 3
    assert all(strategy is not None for strategy in optimizer.strategies)


def test_optimizer_with_custom_strategies():
    """Test optimizer with custom strategies."""
    custom_strategies = [WhitespaceRemoval()]
    optimizer = PromptOptimizer(strategies=custom_strategies)
    assert len(optimizer.strategies) == 1


def test_whitespace_removal_strategy():
    """Test whitespace removal strategy."""
    strategy = WhitespaceRemoval()
    text = "Hello    world\n\n\nThis  has  extra  spaces"
    
    optimized, metadata = strategy.optimize(text)
    
    assert "    " not in optimized
    assert "\n\n\n" not in optimized
    assert metadata["blank_lines_removed"] > 0


def test_redundancy_removal_strategy():
    """Test redundancy removal strategy."""
    strategy = RedundancyRemoval()
    text = "Please can you please write a function for me"
    
    optimized, metadata = strategy.optimize(text)
    
    assert "Please can you please" not in optimized
    assert metadata["phrases_removed"] > 0


def test_constraint_merging_strategy():
    """Test constraint merging strategy."""
    strategy = ConstraintMerging()
    text = "Write a function. The function should be fast. Make the function efficient."
    
    optimized, metadata = strategy.optimize(text)
    
    assert metadata["sentences_merged"] >= 0
    assert len(optimized) <= len(text)


def test_optimizer_pipeline():
    """Test full optimization pipeline."""
    optimizer = PromptOptimizer()
    text = "Please  can  you  please  write  a  function\n\n\nthat  is  fast\n\nMake  it  efficient."
    
    response = optimizer.optimize(text)
    
    assert response.original_text == text
    assert response.optimized_text != text
    assert response.original_tokens > 0
    assert response.optimized_tokens >= 0
    assert response.tokens_saved >= 0
    assert response.percentage_saved >= 0
    assert len(response.strategies_applied) > 0


def test_optimizer_disabled():
    """Test optimizer when disabled."""
    optimizer = PromptOptimizer()
    text = "Test text"
    
    response = optimizer.optimize(text, enable_optimization=False)
    
    assert response.optimized_text == text
    assert response.tokens_saved == 0
    assert response.percentage_saved == 0.0
    assert len(response.strategies_applied) == 0


def test_optimizer_add_strategy():
    """Test adding a strategy to the pipeline."""
    optimizer = PromptOptimizer()
    initial_count = len(optimizer.strategies)
    
    optimizer.add_strategy(WhitespaceRemoval())
    
    assert len(optimizer.strategies) == initial_count + 1


def test_optimizer_remove_strategy():
    """Test removing a strategy from the pipeline."""
    optimizer = PromptOptimizer()
    initial_count = len(optimizer.strategies)
    
    result = optimizer.remove_strategy("WhitespaceRemoval")
    
    assert result is True
    assert len(optimizer.strategies) == initial_count - 1


def test_optimizer_remove_nonexistent_strategy():
    """Test removing a non-existent strategy."""
    optimizer = PromptOptimizer()
    
    result = optimizer.remove_strategy("NonExistentStrategy")
    
    assert result is False


def test_optimization_response_to_dict():
    """Test converting OptimizationResponse to dictionary."""
    response = OptimizationResponse(
        original_text="Original",
        optimized_text="Optimized",
        original_tokens=100,
        optimized_tokens=80,
        tokens_saved=20,
        percentage_saved=20.0,
        strategies_applied=["WhitespaceRemoval"],
        metadata={"test": "value"}
    )
    
    response_dict = response.to_dict()
    
    assert response_dict["original_text"] == "Original"
    assert response_dict["optimized_text"] == "Optimized"
    assert response_dict["original_tokens"] == 100
    assert response_dict["optimized_tokens"] == 80
    assert response_dict["tokens_saved"] == 20
    assert response_dict["percentage_saved"] == 20.0
    assert response_dict["strategies_applied"] == ["WhitespaceRemoval"]
    assert response_dict["metadata"] == {"test": "value"}


def test_optimizer_with_empty_text():
    """Test optimizer with empty text."""
    optimizer = PromptOptimizer()
    text = ""
    
    response = optimizer.optimize(text)
    
    assert response.optimized_text == ""
    assert response.original_tokens == 0
    assert response.optimized_tokens == 0


def test_optimizer_preserves_meaning():
    """Test that optimizer preserves meaning."""
    optimizer = PromptOptimizer()
    text = "Write a Python function that calculates the factorial of a number"
    
    response = optimizer.optimize(text)
    
    # Check that key words are preserved
    assert "Python" in response.optimized_text or "python" in response.optimized_text
    assert "function" in response.optimized_text or "func" in response.optimized_text
    assert "factorial" in response.optimized_text
