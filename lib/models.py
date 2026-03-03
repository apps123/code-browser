from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class RepositorySummary:
    full_name: str
    local_path: Path
    scanned_at: datetime
    total_security_issues: int = 0
    ai_readiness: Optional[str] = None  # "Yes", "No", "Partial"


@dataclass
class OrganizationScanResult:
    org_name: str
    repositories: List[RepositorySummary] = field(default_factory=list)

