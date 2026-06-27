import json
from agents.llm_client import call_llm

def analyze_bug(code: str) -> dict:
    system = """You are an expert Python bug analyzer.
Analyze the given Python code and return ONLY a JSON object with these fields:
- bug_description: what is wrong in the code
- affected_lines: which line numbers have the bug
- fix_approach: how to fix it
Return ONLY JSON, no explanation, no extra text."""

    prompt = f"Analyze this Python code for bugs:\n\n{code}"
    
    response = call_llm(prompt, system=system, temperature=0.1)
    
    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean)
        return result
    except:
        return {"error": "Could not parse response", "raw": response}
    
    