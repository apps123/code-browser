from __future__ import annotations

import logging
from datetime import datetime


class ProgressReporter:
    def __init__(self, logger: logging.Logger | None = None) -> None:
        self._logger = logger or logging.getLogger("repo_analysis.progress")
        self._total = 0
        self._completed = 0

    def start(self, total: int) -> None:
        self._total = total
        self._completed = 0
        self._logger.info("Starting scan of %d repositories", total)

    def increment(self, repo_name: str) -> None:
        self._completed += 1
        self._logger.info(
            "Scanned %s (%d/%d)", repo_name, self._completed, self._total
        )

    def finish(self) -> None:
        self._logger.info("Completed scan of %d repositories", self._total)

    @staticmethod
    def now() -> datetime:
        return datetime.utcnow()

