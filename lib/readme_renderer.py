from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import List, Optional

from .diagram_generator import architecture_diagram, call_graph_diagram, code_organization_diagram
from .repo_analyzer import RepoAnalysis
from .repo_folder_manager import ensure_repo_folder


def _format_date(dt: Optional[datetime]) -> str:
    return dt.isoformat() if dt else "Not available"


def render_readme(
    analysis: RepoAnalysis,
    code_browser_root: Path,
) -> None:
    """
    Render a README.md file for a repository into its code-browser folder.
    """
    repo_dir = ensure_repo_folder(code_browser_root, analysis.summary.full_name)
    readme_path = repo_dir / "README.md"

    lines: List[str] = []
    lines.append(f"# Repository Analysis: {analysis.summary.full_name}")
    lines.append("")
    lines.append("## Scanned Date")
    lines.append("")
    lines.append(f"- {analysis.summary.scanned_at.isoformat()}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Contributor diversity: {', '.join(analysis.contributors) or 'Not available'}")
    lines.append(f"- Tech stack: {', '.join(analysis.tech_stack) or 'Not available'}")
    cov = f"{analysis.code_coverage:.1f}%" if analysis.code_coverage is not None else "Not available"
    lines.append(f"- Code coverage: {cov}")
    lines.append(f"- Total number of security issues: {analysis.summary.total_security_issues}")
    lines.append(f"- Repository README present: {'Yes' if analysis.has_readme else 'No'}")
    lines.append(f"- CI/CD badges: {', '.join(analysis.ci_badges) or 'Not available'}")
    lines.append(f"- Commit recency: {_format_date(analysis.last_updated)}")
    lines.append(f"- Open issues: {analysis.open_issues if analysis.open_issues is not None else 'Not available'}")
    lines.append(
        f"- Closed issues: {analysis.closed_issues if analysis.closed_issues is not None else 'Not available'}"
    )
    lines.append(f"- AI readiness: {analysis.summary.ai_readiness or 'Not available'}")
    lines.append(f"- AI tool support: {', '.join(analysis.ai_tools) or 'Not available'}")
    license_type = analysis.summary.license_type or analysis.license_type or "Not available"
    lines.append(f"- License type: {license_type}")
    lines.append(
        f"- Number of tests available: {analysis.test_count if analysis.test_count is not None else 'Not available'}"
    )
    lines.append("")
    lines.append("## Dependencies")
    lines.append("")
    if analysis.software_dependencies:
        lines.append("- Software Dependencies:")
        for dep in analysis.software_dependencies:
            lines.append(f"  - {dep}")
    else:
        lines.append("- Software Dependencies: Not available")

    if analysis.system_dependencies:
        lines.append("- System Dependencies:")
        for dep in analysis.system_dependencies:
            lines.append(f"  - {dep}")
    else:
        lines.append("- System Dependencies: Not available")
    lines.append("")
    lines.append("## Contribution")
    lines.append("")
    lines.append("- Key Contributors (60%+ combined): Not available")
    lines.append("- All Contributors: Not available")
    lines.append("")
    lines.append("## Architecture")
    lines.append("")
    lines.append(architecture_diagram(analysis.summary.local_path))
    lines.append("")
    lines.append("## Code Organization")
    lines.append("")
    lines.append(code_organization_diagram(analysis.summary.local_path))
    lines.append("")
    lines.append("## Overall Code Flow and Functional Call Graph")
    lines.append("")
    lines.append(call_graph_diagram(analysis.summary.local_path))
    lines.append("")
    lines.append("## Features")
    lines.append("")
    lines.append("- Not available")
    lines.append("")
    lines.append("## Code Documentation")
    lines.append("")
    lines.append("- Not available")
    lines.append("")
    lines.append("## Tests")
    lines.append("")
    lines.append("- Possible Missing Tests: Not available")
    lines.append("- Available Tests: Not available")
    lines.append("")

    readme_path.write_text("\n".join(lines), encoding="utf-8")

