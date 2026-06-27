import os
import ast
from agents.bug_analyzer import analyze_bug
from agents.code_fixer import fix_code
from agents.test_writer import write_tests
from agents.test_runner import run_tests
from agents.pr_agent import create_pr
from db.database import init_db, save_run
from dotenv import load_dotenv

load_dotenv()

def validate_code(code: str) -> tuple:
    # Empty check
    if not code.strip():
        return False, "Code is empty!"
    
    # Valid Python check
    try:
        ast.parse(code)
        return True, "Valid Python!"
    except SyntaxError as e:
        return False, f"Invalid Python syntax: {e}"

def run_pipeline(file_path: str):
    init_db()

    print(f"\n{'='*50}")
    print(f"Bug-to-PR Agent Starting...")
    print(f"File: {file_path}")
    print(f"{'='*50}\n")

    # Step 1 - Read file
    try:
        with open(file_path, "r") as f:
            buggy_code = f.read()
        print("✅ File read successfully!")
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

    # Step 2 - Validate code
    is_valid, message = validate_code(buggy_code)
    if not is_valid:
        print(f"❌ Invalid code: {message}")
        save_run(file_path, "Invalid code", False, "", "failed")
        return None
    print(f"✅ Code validation: {message}")

    # Step 3 - Bug Analyzer
    print("\n🔍 Step 1: Analyzing bug...")
    try:
        bug_report = analyze_bug(buggy_code)
        if not bug_report or "error" in bug_report:
            print("❌ Bug analysis failed!")
            save_run(file_path, "Analysis failed", False, "", "failed")
            return None
        print(f"Bug found: {bug_report.get('bug_description')}")
    except Exception as e:
        print(f"❌ Analyzer error: {e}")
        save_run(file_path, "Analyzer error", False, "", "failed")
        return None

    # Step 4 - Code Fixer
    print("\n🔧 Step 2: Fixing code...")
    try:
        fixed_code = fix_code(buggy_code, bug_report)
        if not fixed_code:
            print("❌ Could not fix code!")
            save_run(file_path, bug_report.get('bug_description'), False, "", "failed")
            return None
        print("Code fixed successfully!")
    except Exception as e:
        print(f"❌ Fixer error: {e}")
        save_run(file_path, bug_report.get('bug_description'), False, "", "failed")
        return None

    # Step 5 - Save fixed code
    os.makedirs("temp_repo", exist_ok=True)
    with open("temp_repo/fixed_code.py", "w") as f:
        f.write(fixed_code)
    print("Fixed code saved!")

    # Step 6 - Test Writer
    print("\n📝 Step 3: Writing tests...")
    try:
        test_code = write_tests(fixed_code)
        if not test_code:
            print("❌ Could not write tests!")
            save_run(file_path, bug_report.get('bug_description'), False, "", "failed")
            return None
        os.makedirs("tests", exist_ok=True)
        with open("tests/test_output.py", "w") as f:
            f.write(test_code)
        print("Tests saved!")
    except Exception as e:
        print(f"❌ Test writer error: {e}")
        return None

    # Step 7 - Test Runner with Retry
    print("\n🧪 Step 4: Running tests...")
    max_retries = 3
    attempt = 0

    while attempt < max_retries:
        print(f"Attempt {attempt + 1} of {max_retries}")
        try:
            result = run_tests()
            if result["passed"]:
                print("✅ All tests passed!")
                break
            else:
                print("❌ Tests failed! Retrying...")
                attempt += 1
                if attempt < max_retries:
                    fixed_code = fix_code(fixed_code, bug_report)
                    test_code = write_tests(fixed_code)
                    with open("tests/test_output.py", "w") as f:
                        f.write(test_code)
                else:
                    print("❌ Max retries reached!")
                    save_run(file_path, bug_report.get('bug_description'), False, "", "failed")
                    return None
        except Exception as e:
            print(f"❌ Test runner error: {e}")
            return None

    # Step 8 - Git + PR
    print("\n🚀 Step 5: Creating PR...")
    try:
        os.chdir("temp_repo")
        os.system("git add fixed_code.py")
        os.system('git commit -m "fix: automated bug fix by Bug-to-PR Agent"')
        os.system(f"git push https://{os.getenv('GITHUB_TOKEN')}@github.com/nandanirunwal/bug-to-pr-test.git bug-fix-branch")
        os.chdir("..")

        pr_url = create_pr(
            branch_name="bug-fix-branch",
            title="fix: automated bug fix by Bug-to-PR Agent",
            body=f"Auto-generated PR\n\nBug: {bug_report.get('bug_description')}\n\nTests: All passed ✅"
        )
    except Exception as e:
        print(f"❌ PR error: {e}")
        pr_url = None

    # Step 9 - Save to database
    save_run(
        input_file=file_path,
        bug_found=bug_report.get('bug_description'),
        fixed=True,
        pr_url=pr_url or "",
        status="success"
    )

    # Step 10 - Summary
    print(f"\n{'='*50}")
    print("PIPELINE COMPLETE!")
    print(f"{'='*50}")
    print(f"Bug: {bug_report.get('bug_description')}")
    print(f"PR: {pr_url}")

    return {
        "bug_report": bug_report,
        "fixed_code": fixed_code,
        "pr_url": pr_url
    }

if __name__ == "__main__":
    result = run_pipeline("test_bug.py")