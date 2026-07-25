import re

from app.llm.base import LLMClient
from app.models import DocClassification, DocType, ExtractedField
from app.parsing.extract_text import ParsedDocument

# Filename-prefix routing: primary classification signal for the shipped
# synthetic fixtures. Checked against the filename (lowercased, no extension)
# using startswith, longest prefix first so e.g. "1099int" wins over "1099".
FILENAME_PREFIX_MAP: list[tuple[str, DocType]] = sorted(
    [
        ("w2", DocType.W2),
        ("1099int", DocType.FORM_1099_INT),
        ("1099div", DocType.FORM_1099_DIV),
        ("1099nec", DocType.FORM_1099_NEC),
        ("1099misc", DocType.FORM_1099_MISC),
        ("k1", DocType.K1),
        ("1098", DocType.FORM_1098),
        ("prior_year_return", DocType.PRIOR_YEAR_RETURN),
    ],
    key=lambda pair: -len(pair[0]),
)

# Text-keyword fallback, for files that don't follow the fixture naming
# convention. Checked as case-insensitive substrings of the extracted text.
TEXT_KEYWORD_MAP: list[tuple[str, DocType]] = [
    ("form w-2", DocType.W2),
    ("form 1099-int", DocType.FORM_1099_INT),
    ("form 1099-div", DocType.FORM_1099_DIV),
    ("form 1099-nec", DocType.FORM_1099_NEC),
    ("form 1099-misc", DocType.FORM_1099_MISC),
    ("schedule k-1", DocType.K1),
    ("form 1098", DocType.FORM_1098),
    ("form 1040", DocType.PRIOR_YEAR_RETURN),
]

ISSUER_FIELD_NAMES = {"employer", "payer", "partnership", "lender", "organization"}
RECIPIENT_FIELD_NAMES = {"employee", "recipient", "partner", "donor", "taxpayer"}
TAX_YEAR_FIELD_NAMES = {"tax year"}

LINE_FIELD_PATTERN = re.compile(r"^([A-Za-z0-9 ()#/'-]+):\s*(.+)$")

READABILITY_TEXT_LENGTH_THRESHOLD = 40
LOW_CONFIDENCE_THRESHOLD = 0.55


class MockLLMClient(LLMClient):
    def classify_and_extract(self, doc: ParsedDocument) -> DocClassification:
        if doc.is_likely_scanned_or_image or len(doc.text.strip()) < READABILITY_TEXT_LENGTH_THRESHOLD:
            return self._classify_unreadable(doc)

        doc_type, type_confidence = self._classify_type(doc)
        fields = self._extract_fields(doc.text)
        issuer = self._find_field_value(fields, ISSUER_FIELD_NAMES)
        recipient = self._find_field_value(fields, RECIPIENT_FIELD_NAMES)
        tax_year = self._find_tax_year(fields)

        warnings: list[str] = []
        if doc_type in (DocType.OTHER, DocType.UNKNOWN):
            warnings.append("Document does not match a recognized tax form type.")

        return DocClassification(
            doc_type=doc_type,
            confidence=type_confidence,
            issuer=issuer,
            recipient_name=recipient,
            tax_year=tax_year,
            fields=fields,
            is_readable=True,
            raw_text_excerpt=doc.text.strip()[:200],
            warnings=warnings,
        )

    def _classify_unreadable(self, doc: ParsedDocument) -> DocClassification:
        return DocClassification(
            doc_type=DocType.UNKNOWN,
            confidence=0.3,
            fields=[],
            is_readable=False,
            raw_text_excerpt=doc.text.strip()[:200] or None,
            warnings=[
                "Low text yield — possible scan quality issue.",
                "Could not confidently identify document type.",
            ],
        )

    def _classify_type(self, doc: ParsedDocument) -> tuple[DocType, float]:
        stem = doc.filename.lower().rsplit(".", 1)[0]
        for prefix, doc_type in FILENAME_PREFIX_MAP:
            if stem.startswith(prefix):
                return doc_type, 0.95

        text_lower = doc.text.lower()
        for keyword, doc_type in TEXT_KEYWORD_MAP:
            if keyword in text_lower:
                return doc_type, 0.8

        # Readable, but not a recognized tax form type (e.g. a donation receipt).
        return DocType.OTHER, 0.9

    def _extract_fields(self, text: str) -> list[ExtractedField]:
        fields: list[ExtractedField] = []
        for line in text.splitlines():
            match = LINE_FIELD_PATTERN.match(line.strip())
            if match:
                name, value = match.group(1).strip(), match.group(2).strip()
                if name and value:
                    fields.append(ExtractedField(name=name, value=value, confidence=0.95))
        return fields

    def _find_field_value(self, fields: list[ExtractedField], names: set[str]) -> str | None:
        for field in fields:
            if field.name.lower() in names:
                return field.value
        return None

    def _find_tax_year(self, fields: list[ExtractedField]) -> int | None:
        for field in fields:
            if field.name.lower() in TAX_YEAR_FIELD_NAMES:
                match = re.search(r"\d{4}", field.value)
                if match:
                    return int(match.group(0))
        return None
