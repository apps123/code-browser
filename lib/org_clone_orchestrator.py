from __future__ import annotations

from pathlib import Path

from .git_providers import GitHubProvider, RepoRef
from .models import OrganizationScanResult, RepositorySummary
from .progress_reporting import ProgressReporter
from .repo_folder_manager import ensure_repo_folder
from .repo_analyzer import RepoAnalyzer
from .readme_renderer import render_readme


def clone_org_repos(
    provider: GitHubProvider,
    org_name: str,
    target_dir: Path,
    reporter: ProgressReporter,
) -> OrganizationScanResult:
    """
    Clone or update all repositories in an organization into the target directory.
    """
    repos = provider.get_organization_repos(org_name)
    reporter.start(len(repos))

    analyzer = RepoAnalyzer()
    result = OrganizationScanResult(org_name=org_name)
    for repo_ref in repos:
        local_path = provider.clone_or_update(repo_ref, target_dir)
        # Ensure a representation folder exists under code-browser/ for this repo.
        ensure_repo_folder(Path("code-browser"), repo_ref.full_name)
        repo_summary = RepositorySummary(
            full_name=repo_ref.full_name,
            local_path=local_path,
            scanned_at=reporter.now(),
        )
        result.repositories.append(repo_summary)
        analysis = analyzer.analyze(repo_ref.full_name, local_path)
        render_readme(analysis, Path("code-browser"))
        reporter.increment(repo_ref.full_name)

    reporter.finish()
    return result

