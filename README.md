 # Bug-to-PR Agent 🤖

An AI-powered agent that automatically detects bugs in Python code, fixes them, writes tests, and creates a GitHub Pull Request.

## How It Works

1. **Bug Analyzer** — Analyzes buggy Python code and identifies the issue
2. **Code Fixer** — Fixes the bug using LLM
3. **Test Writer** — Automatically writes pytest test cases
4. **Test Runner** — Runs tests with automatic retry (up to 3 times)
5. **PR Agent** — Creates a GitHub Pull Request with the fix

## Two Versions

### Version A — Plain Python
- Manual orchestration using `orchestrator.py`
- Retry loop written manually with while loop

### Version B — LangGraph
- Graph-based orchestration using `graph_agent.py`
- Retry loop using conditional edges
- Industry-standard tool

## Tech Stack
- Python 3.14
- Groq API (LLaMA 3.3 70B)
- GitPython
- PyGithub
- LangGraph
- pytest
- Flask
- Streamlit

## Setup

1. Clone the repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate.bat`
4. Install dependencies: `pip install -r requirements.txt`
5. Add API keys in `.env`:
