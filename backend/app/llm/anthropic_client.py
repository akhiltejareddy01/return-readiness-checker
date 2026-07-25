from app.llm.base import LLMClient
from app.models import DocClassification
from app.parsing.extract_text import ParsedDocument


class AnthropicLLMClient(LLMClient):
    """Placeholder for the real Claude-backed implementation.

    Not implemented yet — no ANTHROPIC_API_KEY configured. When ready:
      - Model: claude-opus-4-8 (or claude-sonnet-5 for cost-sensitive volume);
        confirm current availability at implementation time.
      - Use structured output (json_schema matching DocClassification) or a
        forced tool call (e.g. `record_doc_classification`) so the response
        is guaranteed to parse cleanly into DocClassification.
      - For scanned PDFs/images (ParsedDocument.is_likely_scanned_or_image),
        send the raw file bytes as a document/image content block instead of
        (or alongside) extracted text — Claude's vision handles OCR inline.
      - This is a short, single-turn extraction task; low/medium effort output
        config should be sufficient, no extended thinking required.

    Swapping this in is a one-line change in main.py:
        llm_client = AnthropicLLMClient(api_key=...)
    since both implementations satisfy the same LLMClient interface.
    """

    def __init__(self, api_key: str | None = None):
        raise NotImplementedError(
            "AnthropicLLMClient is a placeholder — no API key configured yet. "
            "Use MockLLMClient until ANTHROPIC_API_KEY is available."
        )

    def classify_and_extract(self, doc: ParsedDocument) -> DocClassification:
        raise NotImplementedError
