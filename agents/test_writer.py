import ast
from agents.llm_client import call_llm

def write_tests(fixed_code: str) -> str:
    system = """You are an expert Python test writer.
You write pytest test cases for given Python code.
Return ONLY the test code, no explanation, no markdown backticks.
Just raw Python test code.
Keep the tests concise — write at most 4-5 test functions, covering normal, edge, and error cases."""

    prompt = f"""Write pytest test cases for this Python code:

{fixed_code}

Rules:
- Use pytest
- Test normal cases
- Test edge cases
- Test error cases
- Keep it concise (max 4-5 test functions)
Return ONLY the test code."""

    test_code = call_llm(prompt, system=system, temperature=0.1, max_tokens=2000)

    if not test_code:
        return None

    test_code = test_code.replace("```python", "").replace("```", "").strip()

    # Validate syntax before returning — catch truncated/broken code early
    try:
        ast.parse(test_code)
        return test_code
    except SyntaxError as e:
        print(f"Generated test code has invalid syntax: {e}")
        return None