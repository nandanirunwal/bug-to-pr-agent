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
