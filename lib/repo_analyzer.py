from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

from git import Repo  # type: ignore[import-untyped]

from .models import RepositorySummary
from .security_scanner import SecurityScanner


@dataclass
class RepoAnalysis:
    summary: RepositorySummary
    contributors: List[str]
    tech_stack: List[str]
    code_coverage: Optional[float]
    has_readme: bool
    ci_badges: List[str]
    last_updated: Optional[datetime]
    open_issues: Optional[int]
    closed_issues: Optional[int]
    ai_tools: List[str]
    test_count: Optional[int]
    license_type: Optional[str] = None


class RepoAnalyzer:
    """
    Performs a lightweight analysis of a repository to collect signals needed
    for the generated README.
    """

    def __init__(self, security_scanner: Optional[SecurityScanner] = None) -> None:
        self._security_scanner = security_scanner or SecurityScanner()

    def analyze(self, full_name: str, local_path: Path) -> RepoAnalysis:
        scanned_at = datetime.utcnow()
        security_result = self._security_scanner.run_all(local_path)

        summary = RepositorySummary(
            full_name=full_name,
            local_path=local_path,
            scanned_at=scanned_at,
            total_security_issues=security_result.total_issues,
            ai_readiness=None,
        )

        contributors = self._infer_contributors(local_path)
        tech_stack = self._infer_tech_stack(local_path)
        code_coverage: Optional[float] = None  # left to external coverage tooling
        has_readme = (local_path / "README.md").exists()
        ci_badges: List[str] = []  # detection from README or CI config can be added later
        last_updated = self._infer_last_updated(local_path)
        open_issues: Optional[int] = None
        closed_issues: Optional[int] = None
        ai_tools: List[str] = []  # could be inferred from config files in future
        test_count = self._infer_test_count(local_path)
        license_type = self._infer_license_type(local_path)

        # Simple heuristic for AI readiness based on tests and documentation presence.
        if test_count and test_count > 0 and has_readme:
            summary.ai_readiness = "Yes"
        elif test_count or has_readme:
            summary.ai_readiness = "Partial"
        else:
            summary.ai_readiness = "No"

        summary.license_type = license_type

        return RepoAnalysis(
            summary=summary,
            contributors=contributors,
            tech_stack=tech_stack,
            code_coverage=code_coverage,
            has_readme=has_readme,
            ci_badges=ci_badges,
            last_updated=last_updated,
            open_issues=open_issues,
            closed_issues=closed_issues,
            ai_tools=ai_tools,
            test_count=test_count,
            license_type=license_type,
        )

    def _infer_contributors(self, local_path: Path) -> List[str]:
        try:
            repo = Repo(str(local_path))
        except Exception:
            return []

        counts: Dict[str, int] = {}
        try:
            for commit in repo.iter_commits(max_count=100):
                name = commit.author.name or "Unknown"
                counts[name] = counts.get(name, 0) + 1
        except Exception:
            return []

        total = sum(counts.values()) or 1
        return [f"{name} [{(count/total)*100:.1f}%]" for name, count in counts.items()]

    def _infer_tech_stack(self, local_path: Path) -> List[str]:
        exts: Set[str] = set()
        for path in local_path.rglob("*"):
            if path.is_file():
                exts.add(path.suffix)
        mapping = {
            ".py": "Python",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".java": "Java",
            ".go": "Go",
        }
        stack = {mapping[ext] for ext in exts if ext in mapping}
        return sorted(stack)

    def _infer_last_updated(self, local_path: Path) -> Optional[datetime]:
        try:
            repo = Repo(str(local_path))
            head_commit = next(iter(repo.iter_commits(max_count=1)), None)
            if head_commit is None:
                return None
            return datetime.utcfromtimestamp(head_commit.committed_date)
        except Exception:
            return None

    def _infer_test_count(self, local_path: Path) -> Optional[int]:
        tests_dir = local_path / "tests"
        if not tests_dir.exists():
            return None
        count = 0
        for path in tests_dir.rglob("test_*.py"):
            if path.is_file():
                count += 1
        return count or None

    def _infer_license_type(self, local_path: Path) -> Optional[str]:
        """
        Best-effort detection of the repository license type based on common
        license files in the repository root.
        """
        candidates = [
            "LICENSE",
            "LICENSE.txt",
            "LICENSE.md",
            "COPYING",
            "COPYING.txt",
            "COPYING.md",
        ]

        license_file: Optional[Path] = None
        for name in candidates:
            path = local_path / name
            if path.exists():
                license_file = path
                break

        if not license_file:
            return None

        try:
            text = license_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return None

        lowered = text.lower()

        if "mit license" in lowered:
            return "MIT"
        if "apache license" in lowered:
            if "version 2.0" in lowered:
                return "Apache-2.0"
            return "Apache"
        if "gnu general public license" in lowered:
            if "lesser general public license" in lowered:
                return "LGPL"
            if "affero general public license" in lowered:
                return "AGPL"
            return "GPL"
        if "bsd license" in lowered or "redistribution and use in source and binary forms" in lowered:
            return "BSD"
        if "mozilla public license" in lowered:
            return "MPL"

        return "Custom / Unknown"

