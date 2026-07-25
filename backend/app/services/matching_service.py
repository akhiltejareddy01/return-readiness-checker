import uuid

from app.models import (
    ChecklistItemResult,
    DocType,
    ExtraDocument,
    MatchStatus,
    OpenQuestion,
    OwnerRole,
    ReadinessReport,
    ReadinessVerdict,
    RequestChecklist,
    RequestChecklistItem,
    UploadedDocument,
)

LOW_CONFIDENCE_THRESHOLD = 0.55
STATUS_WEIGHTS = {MatchStatus.RECEIVED: 1.0, MatchStatus.NEEDS_REVIEW: 0.5, MatchStatus.MISSING: 0.0}


def _issuer_matches(hint: str | None, issuer: str | None) -> bool:
    if not hint or not issuer:
        return False
    hint_l, issuer_l = hint.lower(), issuer.lower()
    return hint_l in issuer_l or issuer_l in hint_l


def _select_candidate(
    item: RequestChecklistItem, pool: list[UploadedDocument]
) -> UploadedDocument | None:
    candidates = [d for d in pool if d.classification.doc_type == item.doc_type]
    if not candidates:
        return None
    if item.issuer_hint:
        hinted = [d for d in candidates if _issuer_matches(item.issuer_hint, d.classification.issuer)]
        if hinted:
            return hinted[0]
    if len(candidates) == 1:
        return candidates[0]
    # Multiple ambiguous candidates with no issuer hint match — pick the
    # highest-confidence one and leave the rest to surface as extras.
    # (No interactive reassignment UI in this build; documented simplification.)
    return max(candidates, key=lambda d: d.classification.confidence)


def _build_missing_question(item: RequestChecklistItem) -> OpenQuestion:
    # K-1s are frequently late/complex and often need partner-level follow-up
    # with the issuing entity rather than a generic client chase.
    owner = OwnerRole.PARTNER if item.doc_type == DocType.K1 else OwnerRole.CLIENT
    return OpenQuestion(
        id=str(uuid.uuid4()),
        description=f'"{item.label}" has not been received — follow up to request it.',
        owner=owner,
        related_checklist_item_id=item.id,
    )


def _build_needs_review_question(item: RequestChecklistItem, doc: UploadedDocument) -> OpenQuestion:
    return OpenQuestion(
        id=str(uuid.uuid4()),
        description=(
            f'{doc.filename} was matched to "{item.label}" but is low-confidence or '
            "unreadable — verify manually before counting it as received."
        ),
        owner=OwnerRole.STAFF,
        related_document_id=doc.id,
        related_checklist_item_id=item.id,
    )


def _build_extra_question(doc: UploadedDocument) -> OpenQuestion:
    c = doc.classification
    issuer_note = f" from {c.issuer}" if c.issuer else ""
    return OpenQuestion(
        id=str(uuid.uuid4()),
        description=(
            f"{doc.filename} ({c.doc_type.value}{issuer_note}) received but not on the "
            "request checklist — confirm relevance with client."
        ),
        owner=OwnerRole.STAFF,
        related_document_id=doc.id,
    )


def build_readiness_report(
    checklist: RequestChecklist, uploaded_docs: list[UploadedDocument]
) -> ReadinessReport:
    pool = list(uploaded_docs)
    results: list[ChecklistItemResult] = []
    open_questions: list[OpenQuestion] = []

    for item in checklist.items:
        candidate = _select_candidate(item, pool)

        if candidate is None:
            results.append(
                ChecklistItemResult(
                    item=item, status=MatchStatus.MISSING, reason="Not yet received from client."
                )
            )
            if item.required:
                open_questions.append(_build_missing_question(item))
            continue

        pool.remove(candidate)
        c = candidate.classification
        if (not c.is_readable) or c.confidence < LOW_CONFIDENCE_THRESHOLD:
            results.append(
                ChecklistItemResult(
                    item=item,
                    status=MatchStatus.NEEDS_REVIEW,
                    matched_document_id=candidate.id,
                    reason=(
                        "Document is ambiguous or low-confidence — needs manual review "
                        "before it can be counted as received."
                    ),
                )
            )
            open_questions.append(_build_needs_review_question(item, candidate))
        else:
            results.append(
                ChecklistItemResult(item=item, status=MatchStatus.RECEIVED, matched_document_id=candidate.id)
            )

    extra_documents: list[ExtraDocument] = []
    for doc in pool:
        c = doc.classification
        if (not c.is_readable) or c.doc_type == DocType.UNKNOWN:
            reason = "Document could not be classified or read — confirm with client what this is."
        else:
            reason = "Not on the request checklist — confirm relevance with client."
        extra_documents.append(
            ExtraDocument(document_id=doc.id, filename=doc.filename, doc_type=c.doc_type, reason=reason)
        )
        open_questions.append(_build_extra_question(doc))

    required_results = [r for r in results if r.item.required]
    if required_results:
        score = round(100 * sum(STATUS_WEIGHTS[r.status] for r in required_results) / len(required_results))
    else:
        score = 100

    missing_count = sum(1 for r in required_results if r.status == MatchStatus.MISSING)
    needs_review_count = sum(1 for r in required_results if r.status == MatchStatus.NEEDS_REVIEW)
    ready = missing_count == 0 and needs_review_count == 0

    if ready:
        summary = "READY — all requested documents received and verified."
    else:
        parts = []
        if missing_count:
            parts.append(f"missing {missing_count} item(s)")
        if needs_review_count:
            parts.append(f"{needs_review_count} need review")
        summary = "NOT READY — " + ", ".join(parts)

    verdict = ReadinessVerdict(score=score, ready=ready, summary=summary)

    return ReadinessReport(
        client_name=checklist.client_name,
        tax_year=checklist.tax_year,
        checklist_results=results,
        extra_documents=extra_documents,
        open_questions=open_questions,
        verdict=verdict,
        uploaded_documents=uploaded_docs,
    )
