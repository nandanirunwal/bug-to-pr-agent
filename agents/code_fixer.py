import ast
from agents.llm_client import call_llm

def fix_code(original_code: str, bug_report: dict) -> str:
    system = """You are an expert Python developer.
You will be given buggy Python code and a bug report.
Return ONLY the fixed Python code, no explanation, no extra text, no markdown backticks.
Just return the raw Python code."""

    prompt = f"""Fix this Python code:

{original_code}

Bug Report:
- Bug: {bug_report.get('bug_description')}
- Affected Lines: {bug_report.get('affected_lines')}
- Fix Approach: {bug_report.get('fix_approach')}

Return ONLY the fixed code."""

    fixed_code = call_llm(prompt, system=system, temperature=0.1)
    
    # Remove backticks if LLM added them
    fixed_code = fixed_code.replace("```python", "").replace("```", "").strip()
    
    # Validate syntax
    try:
        ast.parse(fixed_code)
        print("Syntax check passed!")
        return fixed_code
    except SyntaxError as e:
        print(f"Syntax error in fixed code: {e}")
        return None
