from __future__ import annotations

from pathlib import Path


def repo_folder_name(full_name: str) -> str:
    """
    Derive a stable folder name for a repository under code-browser/.

    Uses owner__name (double underscore) to avoid nested directories.
    """
    return full_name.replace("/", "__")


def ensure_repo_folder(code_browser_root: Path, full_name: str) -> Path:
    """
    Ensure a folder exists for the given repository under code-browser/.

    Returns the path to the repository folder.
    """
    repo_dir = code_browser_root / repo_folder_name(full_name)
    repo_dir.mkdir(parents=True, exist_ok=True)
    return repo_dir

