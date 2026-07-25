import io

from pydantic import BaseModel
from pypdf import PdfReader

SCANNED_TEXT_LENGTH_THRESHOLD = 40


class ParsedDocument(BaseModel):
    filename: str
    text: str
    page_count: int
    extraction_method: str  # "pdf-text" | "plain-text" | "image-unsupported"
    is_likely_scanned_or_image: bool


def _parse_pdf(filename: str, content: bytes) -> ParsedDocument:
    reader = PdfReader(io.BytesIO(content))
    pages_text = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages_text)
    return ParsedDocument(
        filename=filename,
        text=text,
        page_count=len(reader.pages),
        extraction_method="pdf-text",
        is_likely_scanned_or_image=len(text.strip()) < SCANNED_TEXT_LENGTH_THRESHOLD,
    )


def parse_document(filename: str, content: bytes) -> ParsedDocument:
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext == "pdf":
        return _parse_pdf(filename, content)
    if ext in ("txt", "md"):
        text = content.decode("utf-8", errors="replace")
        return ParsedDocument(
            filename=filename,
            text=text,
            page_count=1,
            extraction_method="plain-text",
            is_likely_scanned_or_image=len(text.strip()) < SCANNED_TEXT_LENGTH_THRESHOLD,
        )
    if ext in ("png", "jpg", "jpeg"):
        # Real OCR/vision is deferred — this is the plug point for a future
        # AnthropicLLMClient call that sends the raw image bytes directly.
        return ParsedDocument(
            filename=filename,
            text="",
            page_count=1,
            extraction_method="image-unsupported",
            is_likely_scanned_or_image=True,
        )
    raise ValueError(f"Unsupported file type: {filename}")
