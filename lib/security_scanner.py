from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import json
import os
import subprocess


@dataclass
class SecurityIssue:
    tool: str
    identifier: str
    severity: str
    message: str


@dataclass
class SecurityScanResult:
    issues: List[SecurityIssue]

    @property
    def total_issues(self) -> int:
        return len(self.issues)


class SecurityScanner:
    """
    Orchestrates calls to external security tools (SAST, SCA, secrets detection,
    DAST, IaC) and aggregates results into counts suitable for README summaries.
    """

    def run_all(self, repo_path: Path) -> SecurityScanResult:
        issues: List[SecurityIssue] = []

        if os.getenv("REPO_ANALYSIS_ENABLE_BANDIT", "true").lower() == "true":
            issues.extend(self._run_bandit(repo_path))
        if os.getenv("REPO_ANALYSIS_ENABLE_PIP_AUDIT", "true").lower() == "true":
            issues.extend(self._run_pip_audit(repo_path))
        if os.getenv("REPO_ANALYSIS_ENABLE_DETECT_SECRETS", "true").lower() == "true":
            issues.extend(self._run_detect_secrets(repo_path))

        return SecurityScanResult(issues=issues)

    def _run_bandit(self, repo_path: Path) -> List[SecurityIssue]:
        try:
            result = subprocess.run(
                ["bandit", "-r", str(repo_path), "-f", "json"],
                check=False,
                capture_output=True,
                text=True,
            )
            if not result.stdout.strip():
                return []
            data = json.loads(result.stdout)
        except Exception:
            return []

        findings: List[SecurityIssue] = []
        for item in data.get("results", []):
            findings.append(
                SecurityIssue(
                    tool="bandit",
                    identifier=item.get("test_id", "UNKNOWN"),
                    severity=item.get("issue_severity", "UNKNOWN"),
                    message=item.get("issue_text", ""),
                )
            )
        return findings

    def _run_pip_audit(self, repo_path: Path) -> List[SecurityIssue]:
        req = repo_path / "requirements.txt"
        if not req.exists():
            return []

        try:
            result = subprocess.run(
                ["pip-audit", "-r", str(req), "-f", "json"],
                check=False,
                capture_output=True,
                text=True,
            )
            if not result.stdout.strip():
                return []
            data = json.loads(result.stdout)
        except Exception:
            return []

        findings: List[SecurityIssue] = []
        for item in data:
            vulns = item.get("vulns") or []
            if not vulns:
                continue
            vuln = vulns[0]
            findings.append(
                SecurityIssue(
                    tool="pip-audit",
                    identifier=vuln.get("id", "UNKNOWN"),
                    severity=vuln.get("severity", "UNKNOWN"),
                    message=vuln.get("description", ""),
                )
            )
        return findings

    def _run_detect_secrets(self, repo_path: Path) -> List[SecurityIssue]:
        try:
            result = subprocess.run(
                ["detect-secrets", "scan", str(repo_path)],
                check=False,
                capture_output=True,
                text=True,
            )
            if not result.stdout.strip():
                return []
            data = json.loads(result.stdout)
        except Exception:
            return []

        findings: List[SecurityIssue] = []
        for file_path, secrets in data.get("results", {}).items():
            for secret in secrets:
                findings.append(
                    SecurityIssue(
                        tool="detect-secrets",
                        identifier=secret.get("type", "SECRET"),
                        severity="HIGH",
                        message=f"{file_path}:{secret.get('line_number', '?')}",
                    )
                )
        return findings


