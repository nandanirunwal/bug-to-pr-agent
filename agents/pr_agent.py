import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

def create_pr(branch_name: str, title: str, body: str) -> str:
    token = os.getenv("GITHUB_TOKEN")
    repo_name = "nandanirunwal/bug-to-pr-agent"

    if not token:
        print("PR Error: GITHUB_TOKEN not found in environment!")
        return None

    g = Github(token)
    repo = g.get_repo(repo_name)

    try:
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch_name,
            base="main"
        )
        print(f"PR created: {pr.html_url}")
        return pr.html_url
    except Exception as e:
        print(f"PR Error: {e}")
        return None