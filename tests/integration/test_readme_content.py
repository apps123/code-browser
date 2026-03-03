from __future__ import annotations

from pathlib import Path

from lib.readme_renderer import render_readme
from lib.repo_analyzer import RepoAnalysis
from lib.models import RepositorySummary
from datetime import datetime


def test_readme_includes_mermaid_diagrams(tmp_path: Path) -> None:
    code_browser_root = tmp_path / "code-browser"
    code_browser_root.mkdir()

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

    readme_path = code_browser_root / "owner__name" / "README.md"
    content = readme_path.read_text(encoding="utf-8")

    assert "```mermaid" in content

