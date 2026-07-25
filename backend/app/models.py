from enum import Enum
from typing import Optional

from pydantic import BaseModel


class DocType(str, Enum):
    W2 = "W-2"
    FORM_1099_INT = "1099-INT"
    FORM_1099_DIV = "1099-DIV"
    FORM_1099_NEC = "1099-NEC"
    FORM_1099_MISC = "1099-MISC"
    K1 = "K-1"
    FORM_1098 = "1098"
    PRIOR_YEAR_RETURN = "Prior-Year Return"
    OTHER = "Other"
    UNKNOWN = "Unknown"


class RequestChecklistItem(BaseModel):
    id: str
    doc_type: DocType
    label: str
    issuer_hint: Optional[str] = None
    required: bool = True
    notes: Optional[str] = None


class RequestChecklist(BaseModel):
    client_name: str
    tax_year: int
    items: list[RequestChecklistItem]


class ExtractedField(BaseModel):
    name: str
    value: str
    confidence: float = 1.0


class DocClassification(BaseModel):
    doc_type: DocType
    confidence: float
    issuer: Optional[str] = None
    recipient_name: Optional[str] = None
    tax_year: Optional[int] = None
    fields: list[ExtractedField] = []
    is_readable: bool = True
    raw_text_excerpt: Optional[str] = None
    warnings: list[str] = []


class UploadedDocument(BaseModel):
    id: str
    filename: str
    classification: DocClassification


class MatchStatus(str, Enum):
    RECEIVED = "received"
    MISSING = "missing"
    NEEDS_REVIEW = "needs_review"


class ChecklistItemResult(BaseModel):
    item: RequestChecklistItem
    status: MatchStatus
    matched_document_id: Optional[str] = None
    reason: Optional[str] = None


class ExtraDocument(BaseModel):
    document_id: str
    filename: str
    doc_type: DocType
    reason: str


class OwnerRole(str, Enum):
    STAFF = "staff"
    CLIENT = "client"
    PARTNER = "partner"


class OpenQuestion(BaseModel):
    id: str
    description: str
    owner: OwnerRole
    related_document_id: Optional[str] = None
    related_checklist_item_id: Optional[str] = None


class ReadinessVerdict(BaseModel):
    score: int
    ready: bool
    summary: str


class ReadinessReport(BaseModel):
    client_name: str
    tax_year: int
    checklist_results: list[ChecklistItemResult]
    extra_documents: list[ExtraDocument]
    open_questions: list[OpenQuestion]
    verdict: ReadinessVerdict
    uploaded_documents: list[UploadedDocument]


class FollowUpDraftRequest(BaseModel):
    report: ReadinessReport


class FollowUpDraftResponse(BaseModel):
    subject: str
    body: str
