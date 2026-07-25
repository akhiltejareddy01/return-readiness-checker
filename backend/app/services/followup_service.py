from app.models import FollowUpDraftResponse, MatchStatus, ReadinessReport


def build_followup_draft(report: ReadinessReport) -> FollowUpDraftResponse:
    missing = [r.item.label for r in report.checklist_results if r.status == MatchStatus.MISSING]
    needs_review = [r.item.label for r in report.checklist_results if r.status == MatchStatus.NEEDS_REVIEW]

    subject = f"Documents still needed for your {report.tax_year} tax return"

    if report.verdict.ready:
        body = "\n".join(
            [
                f"Hi {report.client_name},",
                "",
                "Great news — we've received and verified everything we need for your "
                f"{report.tax_year} tax return. Your file is ready to move into preparation.",
                "",
                "Thanks,",
                "Your Tax Team",
            ]
        )
        return FollowUpDraftResponse(subject=subject, body=body)

    lines = [
        f"Hi {report.client_name},",
        "",
        "Thanks for the documents you've sent so far! To finish preparing your return, we still need:",
    ]
    lines += [f"  • {label}" for label in missing]

    if needs_review:
        lines += ["", "A couple of items need a clearer copy or quick confirmation:"]
        lines += [f"  • {label}" for label in needs_review]

    lines += [
        "",
        "Once we have these, we'll be ready to move your return into preparation.",
        "",
        "Thanks,",
        "Your Tax Team",
    ]

    return FollowUpDraftResponse(subject=subject, body="\n".join(lines))
