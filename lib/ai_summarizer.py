from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .config import AiProvider


class Summarizer(Protocol):
    def summarize(self, text: str, *, purpose: str) -> str: ...


@dataclass
class AiSummarizer:
    provider: AiProvider

    def summarize(self, text: str, *, purpose: str) -> str:
        """
        Entry point for generating natural‑language summaries.

        The concrete integration with the selected provider (Claude, Cursor, Copilot, etc.)
        is intentionally left to future implementation; for now this is a placeholder that
        preserves the contract.
        """
        # Placeholder implementation: echo input for now.
        return text

