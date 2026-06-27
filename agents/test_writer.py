from agents.llm_client import call_llm

def write_tests(fixed_code: str) -> str:
    system = """You are an expert Python test writer.
You write pytest test cases for given Python code.
Return ONLY the test code, no explanation, no markdown backticks.
Just raw Python test code."""

    prompt = f"""Write pytest test cases for this Python code:

{fixed_code}

Rules:
- Use pytest
- Test normal cases
- Test edge cases
- Test error cases
Return ONLY the test code."""

    test_code = call_llm(prompt, system=system, temperature=0.1)
    test_code = test_code.replace("```python", "").replace("```", "").strip()
    return test_code
