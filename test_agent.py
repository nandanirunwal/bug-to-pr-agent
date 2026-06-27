from agents.pr_agent import create_pr

print("=== Creating PR ===")
pr_url = create_pr(
    branch_name="bug-fix-branch",
    title="fix: automated bug fix by Bug-to-PR Agent",
    body="This PR was automatically created by Bug-to-PR Agent.\n\n- Bug found: Division by zero error\n- Fix applied: Added empty list check\n- Tests: All passed ✅"
)

if pr_url:
    print(f"✅ PR created successfully!")
    print(f"URL: {pr_url}")
else:
    print("❌ PR creation failed!")