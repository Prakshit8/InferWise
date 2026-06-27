"""
Example using the Prompt Analyzer.
"""

from inferwise import InferWise
from inferwise.analyzer import PromptAnalyzer

# Initialize analyzer separately
analyzer = PromptAnalyzer()

# Analyze a coding prompt
coding_messages = [
    {"role": "user", "content": "Write a function to calculate fibonacci numbers in Python"}
]

analysis = analyzer.analyze(coding_messages)

print("=== Coding Task Analysis ===")
print(f"Task: {analysis.task}")
print(f"Language: {analysis.language}")
print(f"Complexity: {analysis.complexity}")
print(f"Estimated Tokens: {analysis.estimated_tokens}")
print(f"Recommended Provider: {analysis.recommended_provider}")
print(f"Optimization Strategy: {analysis.optimization_strategy}")
print(f"Confidence: {analysis.confidence:.2f}")
print(f"Metadata: {analysis.metadata}")
print()

# Analyze a writing task
writing_messages = [
    {"role": "user", "content": "Write an essay about the impact of artificial intelligence on society"}
]

analysis = analyzer.analyze(writing_messages)

print("=== Writing Task Analysis ===")
print(f"Task: {analysis.task}")
print(f"Language: {analysis.language}")
print(f"Complexity: {analysis.complexity}")
print(f"Estimated Tokens: {analysis.estimated_tokens}")
print(f"Recommended Provider: {analysis.recommended_provider}")
print(f"Optimization Strategy: {analysis.optimization_strategy}")
print()

# Use analyzer with InferWise client
print("=== Using Analyzer with InferWise ===")
client = InferWise(provider="groq", enable_analysis=True)

messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Implement a binary search algorithm in JavaScript"},
]

# The analyzer runs automatically during generate()
response = client.generate(messages)

print(f"Response: {response.content}")
print(f"Model: {response.model}")
print(f"Tokens: {response.total_tokens}")
print(f"Cost: ${response.estimated_cost:.6f}")
