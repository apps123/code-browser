from __future__ import annotations

from pathlib import Path

from .git_providers import GitHubProvider, RepoRef
from .repo_folder_manager import ensure_repo_folder
from .repo_analyzer import RepoAnalyzer
from .readme_renderer import render_readme


def clone_single_repo(provider: GitHubProvider, repo_identifier: str, target_dir: Path) -> Path:
    """
    Clone or update a single repository identified by URL or full name.
    """
    if "/" in repo_identifier and repo_identifier.startswith("http"):
        segments = repo_identifier.rstrip("/").split("/")
        owner = segments[-2]
        name = segments[-1]
        full_name = f"{owner}/{name}"
    else:
        full_name = repo_identifier

    repo_ref: RepoRef = provider.get_repo(full_name)
    local_path = provider.clone_or_update(repo_ref, target_dir)
    ensure_repo_folder(Path("code-browser"), full_name)
    analyzer = RepoAnalyzer()
    analysis = analyzer.analyze(full_name, local_path)
    render_readme(analysis, Path("code-browser"))
    return local_path

