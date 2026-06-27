"""
Example using the Prompt Optimizer.
"""

from inferwise.optimizer import PromptOptimizer

# Initialize optimizer
optimizer = PromptOptimizer()

# Optimize a verbose prompt
verbose_prompt = """
Please can you please write a function for me?
Make sure the function is fast.
Also make it efficient.
And don't forget to add error handling.
"""

response = optimizer.optimize(verbose_prompt)

print("=== Original Prompt ===")
print(response.original_text)
print(f"\nTokens: {response.original_tokens}")

print("\n=== Optimized Prompt ===")
print(response.optimized_text)
print(f"\nTokens: {response.optimized_tokens}")

print("\n=== Optimization Analytics ===")
print(f"Tokens Saved: {response.tokens_saved}")
print(f"Percentage Saved: {response.percentage_saved:.2f}%")
print(f"Strategies Applied: {', '.join(response.strategies_applied)}")

print("\n=== Strategy Details ===")
for strategy, metadata in response.metadata.items():
    if not strategy.endswith("_error"):
        print(f"{strategy}: {metadata}")
