import os
import subprocess
import json
import requests
from github import Github

def get_llm_response(prompt, model="llama3.2"):
    # Try Ollama first (local/private)
    try:
        resp = requests.post(
            f"{os.getenv('OLLAMA_HOST', 'http://localhost:11434')}/api/generate",
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=60
        )
        return resp.json()["response"]
    except:
        # Fallback to OpenAI (or Anthropic)
        # Implement similar for openai.ChatCompletion
        pass

# Main logic
g = Github(os.getenv("GITHUB_TOKEN"))
repo = g.get_repo(os.getenv("GITHUB_REPOSITORY"))
pr = repo.get_pull(int(os.getenv("PR_NUMBER", 0))) if "pull_request" in os.environ else None

# Get diff
diff = subprocess.check_output(["git", "diff", "HEAD^"]).decode()

prompt = f"""You are a senior AppSec engineer. Analyze this code diff for security issues:

{diff}

Also consider these scanner findings (Trivy/Semgrep/CodeQL):
[Insert summarized JSON from previous steps]

Provide:
1. Critical/High risk issues with line numbers.
2. Context-aware explanation (why it's risky in this app).
3. Remediation code snippet.
4. Overall risk score (1-10) and confidence.

Output in clean Markdown for GitHub comment.
"""

response = get_llm_response(prompt)

if pr:
    pr.create_issue_comment(f"## 🤖 AI Security Review\n\n{response}")
