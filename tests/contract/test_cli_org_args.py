from __future__ import annotations

from typer.testing import CliRunner

from cli.repo_analysis_cli import app


runner = CliRunner()


def test_org_scan_requires_org_url() -> None:
    result = runner.invoke(app, ["org-scan"])
    assert result.exit_code != 0
    assert "--org-url" in result.output

