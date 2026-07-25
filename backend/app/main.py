import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS
from app.llm.base import LLMClient
from app.llm.mock_client import MockLLMClient
from app.models import FollowUpDraftRequest, FollowUpDraftResponse, ReadinessReport, RequestChecklist, UploadedDocument
from app.parsing.extract_text import parse_document
from app.services.checklist_service import load_checklist
from app.services.followup_service import build_followup_draft
from app.services.matching_service import build_readiness_report

app = FastAPI(title="Return Readiness Checker")

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Swap for AnthropicLLMClient() once ANTHROPIC_API_KEY is available — both
# implementations satisfy the same LLMClient interface.
llm_client: LLMClient = MockLLMClient()


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/checklist", response_model=RequestChecklist)
def get_checklist() -> RequestChecklist:
    return load_checklist()


@app.post("/api/analyze", response_model=ReadinessReport)
async def analyze(files: list[UploadFile] = File(...)) -> ReadinessReport:
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    checklist = load_checklist()
    uploaded_docs: list[UploadedDocument] = []

    for upload in files:
        content = await upload.read()
        try:
            parsed = parse_document(upload.filename or "unknown", content)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        classification = llm_client.classify_and_extract(parsed)
        uploaded_docs.append(
            UploadedDocument(id=str(uuid.uuid4()), filename=upload.filename or "unknown", classification=classification)
        )

    return build_readiness_report(checklist, uploaded_docs)


@app.post("/api/followup-draft", response_model=FollowUpDraftResponse)
def followup_draft(req: FollowUpDraftRequest) -> FollowUpDraftResponse:
    return build_followup_draft(req.report)
