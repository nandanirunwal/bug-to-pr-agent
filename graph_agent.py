from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.bug_analyzer import analyze_bug
from agents.code_fixer import fix_code
from agents.test_writer import write_tests
from agents.test_runner import run_tests
from agents.pr_agent import create_pr
from agents.git_agent import init_repo, setup_remote_with_token, create_branch, commit_changes, push_branch
import os

# State define karo
class BugToPRState(TypedDict):
    code: str
    bug_report: dict
    fixed_code: str
    test_code: str
    test_result: str
    retry_count: int
    pr_url: str

# Node 1 - Bug Analyzer
def analyzer_node(state: BugToPRState) -> dict:
    print("🔍 Analyzing bug...")
    bug_report = analyze_bug(state["code"])
    print(f"Bug found: {bug_report.get('bug_description')}")
    return {"bug_report": bug_report}

# Node 2 - Code Fixer
def fixer_node(state: BugToPRState) -> dict:
    print("🔧 Fixing code...")
    fixed_code = fix_code(state["code"], state["bug_report"])
    print("Code fixed!")
    return {
        "fixed_code": fixed_code,
        "retry_count": state["retry_count"] + 1
    }

# Node 3 - Test Writer
def test_writer_node(state: BugToPRState) -> dict:
    print("📝 Writing tests...")
    test_code = write_tests(state["fixed_code"])
    os.makedirs("tests", exist_ok=True)
    with open("tests/test_output.py", "w") as f:
        f.write(test_code)
    print("Tests saved!")
    return {"test_code": test_code}

# Node 4 - Test Runner
def test_runner_node(state: BugToPRState) -> dict:
    print("🧪 Running tests...")
    result = run_tests()
    status = "passed" if result["passed"] else "failed"
    print(f"Tests: {status}")
    return {"test_result": status}

# Node 5 - PR Node
def pr_node(state: BugToPRState) -> dict:
    print("🚀 Creating PR...")

    try:
        os.makedirs("temp_repo", exist_ok=True)

        # Fixed code save karo temp_repo mein
        with open("temp_repo/fixed_code.py", "w") as f:
            f.write(state["fixed_code"])

        # Git setup — apna git_agent.py wala proper logic use karo
        repo = init_repo("temp_repo")
        setup_remote_with_token(repo, repo_name="nandanirunwal/bug-to-pr-agent")
        create_branch(repo, "bug-fix-branch")
        commit_changes(repo, ["fixed_code.py"], "fix: automated bug fix by Bug-to-PR Agent")
        push_branch(repo, "bug-fix-branch")

        # PR create karo
        pr_url = create_pr(
            branch_name="bug-fix-branch",
            title="fix: automated bug fix by Bug-to-PR Agent",
            body=f"Auto-generated PR\n\nBug: {state['bug_report'].get('bug_description')}\n\nTests: All passed ✅"
        )

        print(f"PR: {pr_url}")
        return {"pr_url": pr_url or "PR creation failed - check logs"}

    except Exception as e:
        print(f"PR NODE ERROR: {e}")
        return {"pr_url": f"Error: {e}"}

# Conditional Edge
def should_retry(state: BugToPRState) -> str:
    if state["test_result"] == "passed":
        return "passed"
    elif state["retry_count"] >= 3:
        return "max_retries"
    else:
        return "retry"

# Graph banao
graph = StateGraph(BugToPRState)

# Nodes add karo
graph.add_node("analyzer", analyzer_node)
graph.add_node("fixer", fixer_node)
graph.add_node("test_writer", test_writer_node)
graph.add_node("test_runner", test_runner_node)
graph.add_node("pr", pr_node)

# Edges add karo
graph.set_entry_point("analyzer")
graph.add_edge("analyzer", "fixer")
graph.add_edge("fixer", "test_writer")
graph.add_edge("test_writer", "test_runner")

# Conditional edge
graph.add_conditional_edges(
    "test_runner",
    should_retry,
    {
        "passed": "pr",
        "retry": "fixer",
        "max_retries": END
    }
)
graph.add_edge("pr", END)

# Compile karo
app = graph.compile()

# Test karo
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    with open("test_bug.py", "r") as f:
        buggy_code = f.read()

    print("Graph shuru ho raha hai...\n")
    result = app.invoke({
        "code": buggy_code,
        "bug_report": {},
        "fixed_code": "",
        "test_code": "",
        "test_result": "",
        "retry_count": 0,
        "pr_url": ""
    })

    print(f"\n{'='*50}")
    print("GRAPH COMPLETE!")
    print(f"Test Result: {result['test_result']}")
    print(f"PR URL: {result['pr_url']}")