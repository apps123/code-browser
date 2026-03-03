from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import typer

from lib.config import AiProvider, CliConfig, resolve_workdir
from lib.git_providers import GitHubProvider
from lib.logging_config import configure_logging
from lib.org_clone_orchestrator import clone_org_repos
from lib.progress_reporting import ProgressReporter
from lib.repo_clone import clone_single_repo


app = typer.Typer(help="Repository analysis CLI for generating code-browser READMEs.")


def _build_config(
    org_url: Optional[str],
    repo_url: Optional[str],
    workdir: Optional[str],
    ai_provider: AiProvider,
) -> CliConfig:
    token = os.environ.get("GITHUB_TOKEN") or ""
    base_url = os.environ.get("GITHUB_BASE_URL")
    if not token:
        raise typer.BadParameter("GITHUB_TOKEN environment variable must be set.")

    return CliConfig(
        org_url=org_url,
        repo_url=repo_url,
        workdir=resolve_workdir(workdir),
        ai_provider=ai_provider,
        github_token=token,
        github_base_url=base_url,
    )


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", help="Enable verbose logging (DEBUG level)."),
) -> None:
    if verbose:
        configure_logging(level=logging.DEBUG)
    else:
        configure_logging()


@app.command("org-scan")
def org_scan(
    org_url: str = typer.Option(..., "--org-url", help="GitHub or Enterprise org URL or name."),
    workdir: Optional[str] = typer.Option(
        None,
        "--workdir",
        help="Working directory for clones; defaults to ./work",
    ),
    ai_provider: AiProvider = typer.Option(
        AiProvider.CLAUDE,
        "--ai-provider",
        case_sensitive=False,
        help="Local AI assistant to use for summarization.",
    ),
) -> None:
    """
    Scan all repositories in an organization and prepare for analysis.
    """
    cfg = _build_config(org_url=org_url, repo_url=None, workdir=workdir, ai_provider=ai_provider)
    gh = GitHubProvider(token=cfg.github_token, base_url=cfg.github_base_url)
    reporter = ProgressReporter()
    clone_org_repos(gh, _extract_org_name(org_url), Path(cfg.workdir), reporter)


@app.command("repo-scan")
def repo_scan(
    repo_url: str = typer.Option(..., "--repo-url", help="GitHub or Enterprise repo URL or full name."),
    workdir: Optional[str] = typer.Option(
        None,
        "--workdir",
        help="Working directory for clones; defaults to ./work",
    ),
    ai_provider: AiProvider = typer.Option(
        AiProvider.CLAUDE,
        "--ai-provider",
        case_sensitive=False,
        help="Local AI assistant to use for summarization.",
    ),
) -> None:
    """
    Scan a single repository and prepare for analysis.
    """
    cfg = _build_config(org_url=None, repo_url=repo_url, workdir=workdir, ai_provider=ai_provider)
    gh = GitHubProvider(token=cfg.github_token, base_url=cfg.github_base_url)
    clone_single_repo(gh, repo_url, Path(cfg.workdir))


def _extract_org_name(org_url_or_name: str) -> str:
    if "/" not in org_url_or_name:
        return org_url_or_name
    return org_url_or_name.rstrip("/").split("/")[-1]


def _extract_repo_full_name(url_or_name: str) -> str:
    if "/" in url_or_name and url_or_name.startswith("http"):
        segments = url_or_name.rstrip("/").split("/")
        owner = segments[-2]
        name = segments[-1]
        return f"{owner}/{name}"
    return url_or_name


if __name__ == "__main__":
    app()

