# -----------------------------
# core/github_utils.py
# -----------------------------
import os
from github import Github

def get_repo_info(repo_name="openai/whisper", token=None):
    """
    Busca informações do repositório GitHub.

    Args:
        repo_name (str): Nome do repositório no formato 'owner/repo'.
        token (str, optional): Token de autenticação GitHub.

    Returns:
        dict: Informações do repositório.
    """
    try:
        if token:
            g = Github(token)
        else:
            g = Github()  # Anônimo (rate limit reduzido)

        repo = g.get_repo(repo_name)
        return {
            "name": repo.full_name,
            "description": repo.description,
            "language": repo.language,
            "stars": repo.stargazers_count,
            "open_issues": repo.open_issues_count,
            "last_commit": repo.get_commits()[0].commit.message
        }

    except Exception as e:
        return {
            "error": str(e)
        }