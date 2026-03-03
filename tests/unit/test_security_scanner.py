from __future__ import annotations

from pathlib import Path

from lib.security_scanner import SecurityScanner, SecurityIssue, SecurityScanResult


def test_security_scanner_returns_zero_issues_for_now(tmp_path: Path) -> None:
    scanner = SecurityScanner()
    result = scanner.run_all(tmp_path)
    assert result.total_issues == 0


def test_security_scan_result_total_issues_counts_entries() -> None:
    issues = [
        SecurityIssue(tool="bandit", identifier="B101", severity="LOW", message="Example"),
        SecurityIssue(tool="bandit", identifier="B102", severity="MEDIUM", message="Example 2"),
    ]
    result = SecurityScanResult(issues=issues)
    assert result.total_issues == 2

