"""
Example using the Model Router.
"""

from inferwise.router import ModelRouter, RoutingPolicy

# Initialize router with default policy
router = ModelRouter(default_policy=RoutingPolicy.BALANCED)

# Route for a simple coding task
print("=== Simple Coding Task ===")
response = router.route(
    task="coding",
    complexity="low",
    context_size=1000
)

print(f"Selected Provider: {response.selected_provider}")
print(f"Selected Model: {response.selected_model}")
print(f"Routing Reason: {response.routing_reason}")
print(f"Scores: {response.scores}")

# Route for a complex analysis task
print("\n=== Complex Analysis Task ===")
response = router.route(
    task="analysis",
    complexity="high",
    context_size=5000,
    policy=RoutingPolicy.QUALITY_OPTIMIZED
)

print(f"Selected Provider: {response.selected_provider}")
print(f"Selected Model: {response.selected_model}")
print(f"Routing Reason: {response.routing_reason}")
print(f"Scores: {response.scores}")

# Route with cost optimization
print("\n=== Cost-Optimized Routing ===")
response = router.route(
    task="general",
    complexity="low",
    context_size=500,
    policy=RoutingPolicy.COST_OPTIMIZED
)

print(f"Selected Provider: {response.selected_provider}")
print(f"Selected Model: {response.selected_model}")
print(f"Routing Reason: {response.routing_reason}")
print(f"Scores: {response.scores}")

# Custom routing policy
print("\n=== Custom Routing Policy ===")

def custom_policy(task, complexity, context_size):
    """Custom policy: always use Groq for coding, OpenAI for everything else."""
    if task == "coding":
        return "groq"
    return "openai"

response = router.route(
    task="coding",
    complexity="high",
    context_size=2000,
    custom_policy=custom_policy
)

print(f"Selected Provider: {response.selected_provider}")
print(f"Routing Reason: {response.routing_reason}")
