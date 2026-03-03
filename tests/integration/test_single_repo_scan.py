from __future__ import annotations

from typer.testing import CliRunner

from cli.repo_analysis_cli import app


runner = CliRunner()


def test_repo_scan_help() -> None:
    result = runner.invoke(app, ["repo-scan", "--help"])
    assert result.exit_code == 0
    assert "repo-scan" in result.output

