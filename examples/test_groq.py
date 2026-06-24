print("Starting...")

from inferwise.llm import call_llm

print("Imported successfully")

messages = [
    {
        "role": "user",
        "content": "What is machine learning?"
    }
]

print("Calling Groq...")

response = call_llm(messages)

print("Got response!")
print(response)