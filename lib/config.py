from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class AiProvider(str, Enum):
    CLAUDE = "claude"
    CURSOR = "cursor"
    COPILOT = "copilot"
    OTHER = "other"


@dataclass
class CliConfig:
    org_url: Optional[str]
    repo_url: Optional[str]
    workdir: Path
    ai_provider: AiProvider
    github_token: str
    github_base_url: Optional[str] = None


def resolve_workdir(workdir: Optional[str]) -> Path:
    if workdir:
        return Path(workdir).expanduser().resolve()
    return Path("work").resolve()

