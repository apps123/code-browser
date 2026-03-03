from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

from git import Repo  # type: ignore[import-untyped]
from github import Github, Organization, Repository  # type: ignore[import-untyped]


@dataclass
class RepoRef:
    full_name: str
    ssh_url: str
    clone_url: str
    default_branch: str


class GitHubProvider:
    """
    Thin wrapper over PyGithub and GitPython for organization and repository operations.

    This module focuses on local cloning/updating and basic metadata. Higher-level
    orchestration (e.g., analysis, README generation) lives elsewhere.
    """

    def __init__(self, token: str, base_url: Optional[str] = None) -> None:
        if base_url:
            self._gh = Github(login_or_token=token, base_url=base_url.rstrip("/"))
        else:
            self._gh = Github(login_or_token=token)

    def get_organization_repos(self, org_name: str) -> List[RepoRef]:
        org: Organization.Organization = self._gh.get_organization(org_name)  # type: ignore[attr-defined]
        repos: Iterable[Repository.Repository] = org.get_repos()  # type: ignore[attr-defined]
        results: List[RepoRef] = []
        for repo in repos:
            results.append(
                RepoRef(
                    full_name=repo.full_name,
                    ssh_url=repo.ssh_url,
                    clone_url=repo.clone_url,
                    default_branch=repo.default_branch or "main",
                )
            )
        return results

    def get_repo(self, full_name: str) -> RepoRef:
        repo: Repository.Repository = self._gh.get_repo(full_name)  # type: ignore[attr-defined]
        return RepoRef(
            full_name=repo.full_name,
            ssh_url=repo.ssh_url,
            clone_url=repo.clone_url,
            default_branch=repo.default_branch or "main",
        )

    @staticmethod
    def clone_or_update(repo_ref: RepoRef, target_dir: Path) -> Path:
        """
        Clone the repository into target_dir if missing, otherwise fetch and fast‑forward.
        """
        target_dir.mkdir(parents=True, exist_ok=True)
        repo_path = target_dir / repo_ref.full_name.replace("/", "__")

        if repo_path.exists():
            repo = Repo(str(repo_path))
            origin = repo.remotes.origin
            origin.fetch()
            repo.git.checkout(repo_ref.default_branch)
            repo.git.pull("--ff-only")
        else:
            Repo.clone_from(repo_ref.clone_url, str(repo_path), branch=repo_ref.default_branch)

        return repo_path

