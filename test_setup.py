from agents.llm_client import call_llm

# Test 1 - Simple prompt
print("=== Test 1: Simple ===")
response = call_llm("What is a software bug? Answer in 2 lines.")
print(response)

# Test 2 - Strict system prompt
print("\n=== Test 2: Strict System Prompt ===")
response = call_llm(
    prompt="What is a software bug?",
    system="You are a strict technical assistant. Answer in exactly 1 line, no extra words."
)
print(response)

# Test 3 - Creative (high temperature)
print("\n=== Test 3: Creative ===")
response = call_llm(
    prompt="Explain a software bug in a funny way.",
    temperature=0.9
)
print(response)

print("\nDay 2 Complete!")
import os
os.makedirs("logs", exist_ok=True)
with open("logs/day2_output.txt", "w") as f:
    f.write(response)
print("Log saved!")
