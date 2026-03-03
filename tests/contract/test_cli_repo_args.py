from __future__ import annotations

from typer.testing import CliRunner

from cli.repo_analysis_cli import app


runner = CliRunner()


def test_repo_scan_requires_repo_url() -> None:
    result = runner.invoke(app, ["repo-scan"])
    assert result.exit_code != 0
    assert "--repo-url" in result.output

