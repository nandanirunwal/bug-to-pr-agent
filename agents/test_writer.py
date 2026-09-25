import ast
from agents.llm_client import call_llm

def write_tests(fixed_code: str) -> str:
    system = """You are an expert Python test writer.
You write pytest test cases for given Python code.
Return ONLY the test code, no explanation, no markdown backticks.
Just raw Python test code.

IMPORTANT — the code you are testing is a SCRIPT with hardcoded values already in it (not a reusable function).
Because the values are hardcoded inside the script, you CANNOT and MUST NOT try to inject or override variables
before running it — the script will just reset them to its own hardcoded values anyway.

Instead, follow this exact pattern:
1. Assign the literal script source code (exactly as given) to a variable called SOURCE_CODE, using a triple-quoted string.
2. Write exactly ONE test function that runs the script using exec(SOURCE_CODE, {}, {}) inside a pytest capsys fixture,
   captures the printed stdout using capsys.readouterr(), and asserts that the captured output matches the correct
   expected result, which you must calculate yourself by mentally executing the script's hardcoded logic.
3. If the script's hardcoded input would naturally cause an error to be printed (like a custom error message),
   assert that the expected error message appears in the captured output instead of a numeric result.
4. Do not attempt to parametrize with different input values — since this is a script with fixed hardcoded values,
   there is only ONE meaningful test case: running it exactly as-is and checking its output.
5. Keep it extremely simple — just ONE test function, no more.
"""

    prompt = f"""Write a pytest test for this Python script (it has hardcoded values, do not try to change them):

{fixed_code}

Rules:
- Follow the exec-based pattern described in the system instructions exactly
- Write exactly ONE test function
- Run the script as-is with exec(SOURCE_CODE, {{}}, {{}}) and check captured stdout via capsys
- Calculate the correct expected output yourself based on the script's hardcoded values
Return ONLY the test code."""

    test_code = call_llm(prompt, system=system, temperature=0.1, max_tokens=1500)

    if not test_code:
        return None

    test_code = test_code.replace("```python", "").replace("```", "").strip()

    try:
        ast.parse(test_code)
        return test_code
    except SyntaxError as e:
        print(f"Generated test code has invalid syntax: {e}")
        return None