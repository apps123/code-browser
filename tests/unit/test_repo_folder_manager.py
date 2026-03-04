from __future__ import annotations

from pathlib import Path

from lib.repo_folder_manager import ensure_repo_folder, repo_folder_name


def test_repo_folder_name_replaces_slash() -> None:
    assert repo_folder_name("owner/name") == "owner__name"


def test_ensure_repo_folder_creates_directory(tmp_path: Path) -> None:
    root = tmp_path / "code-browser"
    full_name = "owner/name"

    repo_dir = ensure_repo_folder(root, full_name)

    assert repo_dir.exists()
    assert repo_dir.is_dir()
    assert repo_dir.name == "owner__name"

