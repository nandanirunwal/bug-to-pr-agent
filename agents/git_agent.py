import git
import os

def init_repo(path: str = ".") -> git.Repo:
    try:
        repo = git.Repo(path)
        print("Existing repo found!")
    except:
        repo = git.Repo.init(path)
        print("New repo initialized!")
    return repo

def setup_remote_with_token(repo: git.Repo, repo_name: str = "nandanirunwal/bug-to-pr-agent") -> None:
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("ERROR: GITHUB_TOKEN not found in environment!")
        raise ValueError("GITHUB_TOKEN is missing")

    remote_url = f"https://{token}@github.com/{repo_name}.git"

    if "origin" in [r.name for r in repo.remotes]:
        repo.delete_remote("origin")
    repo.create_remote("origin", remote_url)
    print("Remote 'origin' configured with token.")

def create_branch(repo: git.Repo, branch_name: str) -> None:
    if branch_name in repo.heads:
        repo.heads[branch_name].checkout()
        print(f"Switched to existing branch: {branch_name}")
    else:
        repo.git.checkout("-b", branch_name)
        print(f"New branch created: {branch_name}")

def commit_changes(repo: git.Repo, files: list, message: str) -> None:
    repo.index.add(files)
    repo.index.commit(message)
    print(f"Committed: {message}")

def push_branch(repo: git.Repo, branch_name: str, remote_name: str = "origin") -> None:
    try:
        origin = repo.remote(name=remote_name)
        origin.push(refspec=f"{branch_name}:{branch_name}", force=True)
        print(f"Pushed branch to GitHub: {branch_name}")
    except Exception as e:
        print(f"PUSH ERROR: {e}")
        raise