from __future__ import annotations

from lib.ai_summarizer import AiSummarizer
from lib.config import AiProvider


def test_ai_summarizer_echoes_text_for_now() -> None:
    summarizer = AiSummarizer(provider=AiProvider.CLAUDE)
    text = "Sample text"
    result = summarizer.summarize(text, purpose="test")
    assert result == text


def test_ai_summarizer_handles_empty_text() -> None:
    summarizer = AiSummarizer(provider=AiProvider.CURSOR)
    result = summarizer.summarize("", purpose="empty")
    assert result == ""

