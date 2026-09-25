import ast
from agents.llm_client import call_llm

def write_tests(fixed_code: str) -> str:
    system = """You are an expert Python test writer.
You write pytest test cases for given Python code.
Return ONLY the test code, no explanation, no markdown backticks.
Just raw Python test code.

IMPORTANT — the code you are testing is a SCRIPT (top-level statements with variables), not a function.
To test a script safely:
1. Write a helper that takes the input values you want to test, builds a dictionary of those variables directly (e.g. {"marks": [80, 90, 100]}), and passes that dictionary as the exec() locals/globals directly — do NOT use string replace or placeholder tricks like "__varname__".
2. Example pattern to follow exactly:

def run_code(marks):
    local_ns = {"marks": marks}
    exec(SOURCE_CODE, {}, local_ns)
    return local_ns.get("average")

Where SOURCE_CODE is the literal code under test, assigned to a variable at the top of the test file.
3. Keep it concise — write at most 4 test functions covering normal, edge, and error cases.
"""

    prompt = f"""Write pytest test cases for this Python script:

{fixed_code}

Rules:
- Follow the exec-based testing pattern described in the system instructions exactly
- Directly assign real input values into the exec namespace dictionary — never use placeholder/replace tricks
- Test normal cases, edge cases (like empty input), and error cases
- Keep it concise (max 4 test functions)
Return ONLY the test code."""

    test_code = call_llm(prompt, system=system, temperature=0.1, max_tokens=2000)

    if not test_code:
        return None

    test_code = test_code.replace("```python", "").replace("```", "").strip()

    try:
        ast.parse(test_code)
        return test_code
    except SyntaxError as e:
        print(f"Generated test code has invalid syntax: {e}")
        return None