import subprocess

def run_tests() -> dict:
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/test_output.py", "-v"],
        capture_output=True,
        text=True
    )
    
    passed = result.returncode == 0
    
    return {
        "passed": passed,
        "output": result.stdout,
        "errors": result.stderr
    }
