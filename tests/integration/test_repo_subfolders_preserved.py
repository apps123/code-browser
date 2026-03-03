from __future__ import annotations

from pathlib import Path

from lib.readme_renderer import render_readme
from lib.repo_analyzer import RepoAnalysis
from lib.models import RepositorySummary
from datetime import datetime


def test_subfolders_preserved_across_render(tmp_path: Path) -> None:
    code_browser_root = tmp_path / "code-browser"
    repo_dir = code_browser_root / "owner__name"
    docs_dir = repo_dir / "Documentation"
    features_dir = repo_dir / "Features"
    docs_dir.mkdir(parents=True)
    features_dir.mkdir(parents=True)

    (docs_dir / "README.md").write_text("Docs", encoding="utf-8")
    (features_dir / "features.md").write_text("Features", encoding="utf-8")

    summary = RepositorySummary(
        full_name="owner/name",
        local_path=tmp_path,
        scanned_at=datetime.utcnow(),
    )
    analysis = RepoAnalysis(
        summary=summary,
        contributors=[],
        tech_stack=[],
        code_coverage=None,
        has_readme=False,
        ci_badges=[],
        last_updated=None,
        open_issues=None,
        closed_issues=None,
        ai_tools=[],
        test_count=None,
    )

    render_readme(analysis, code_browser_root)

    assert (docs_dir / "README.md").read_text(encoding="utf-8") == "Docs"
    assert (features_dir / "features.md").read_text(encoding="utf-8") == "Features"

