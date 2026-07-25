"""Generates synthetic tax-document PDF fixtures for the Return Readiness Checker demo.

Run: python data/fixtures/generate_fixtures.py
Output is committed to data/fixtures/generated/ so the demo works without
re-running this script. All names/numbers are fabricated — no real PII.
"""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

OUTPUT_DIR = Path(__file__).resolve().parent / "generated"

TAXPAYER = "Jordan Ellis"
TAX_YEAR = 2024


def _write_lines_pdf(path: Path, title: str, lines: list[str]) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 72

    c.setFont("Helvetica-Bold", 14)
    c.drawString(72, y, title)
    y -= 28

    c.setFont("Helvetica", 11)
    for line in lines:
        c.drawString(72, y, line)
        y -= 20

    c.showPage()
    c.save()


def generate_w2() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "w2_acme_robotics.pdf",
        "Form W-2 Wage and Tax Statement",
        [
            f"Tax Year: {TAX_YEAR}",
            "Employer: Acme Robotics Inc.",
            f"Employee: {TAXPAYER}",
            "Box 1 Wages: $82,340.00",
            "Box 2 Federal Tax Withheld: $11,204.50",
        ],
    )


def generate_1099_int() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "1099int_chase_bank.pdf",
        "Form 1099-INT",
        [
            f"Tax Year: {TAX_YEAR}",
            "Payer: Chase Bank N.A.",
            f"Recipient: {TAXPAYER}",
            "Box 1 Interest Income: $412.18",
        ],
    )


def generate_1099_div() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "1099div_fidelity.pdf",
        "Form 1099-DIV",
        [
            f"Tax Year: {TAX_YEAR}",
            "Payer: Fidelity Investments",
            f"Recipient: {TAXPAYER}",
            "Box 1a Ordinary Dividends: $1,205.33",
        ],
    )


def generate_1099_nec() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "1099nec_globex_consulting.pdf",
        "Form 1099-NEC",
        [
            f"Tax Year: {TAX_YEAR}",
            "Payer: Globex Consulting LLC",
            f"Recipient: {TAXPAYER}",
            "Box 1 Nonemployee Compensation: $6,500.00",
        ],
    )


def generate_k1() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "k1_riverside_partners.pdf",
        "Schedule K-1 (Form 1065)",
        [
            f"Tax Year: {TAX_YEAR}",
            "Partnership: Riverside Partners LP",
            f"Partner: {TAXPAYER}",
            "Box 1 Ordinary Business Income: $18,204.00",
        ],
    )


def generate_1098() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "1098_wellsfargo_mortgage.pdf",
        "Form 1098 Mortgage Interest Statement",
        [
            f"Tax Year: {TAX_YEAR}",
            "Lender: Wells Fargo Home Mortgage",
            f"Recipient: {TAXPAYER}",
            "Box 1 Mortgage Interest Received: $9,842.11",
        ],
    )


def generate_prior_year_return() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "prior_year_return_1040_2024.pdf",
        "Form 1040 — U.S. Individual Income Tax Return",
        [
            f"Tax Year: {TAX_YEAR - 1}",
            f"Taxpayer: {TAXPAYER}",
            "AGI: $94,120.00",
        ],
    )


def generate_ambiguous() -> None:
    # Deliberately near-blank so pypdf extracts almost no text, simulating a
    # low-quality scan. This triggers the parsing layer's
    # is_likely_scanned_or_image heuristic and the mock LLM's unreadable path.
    c = canvas.Canvas(str(OUTPUT_DIR / "ambiguous_scan_lowquality.pdf"), pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 8)
    c.drawString(300, height / 2, "xJ2")
    c.showPage()
    c.save()


def generate_extra_unexpected() -> None:
    _write_lines_pdf(
        OUTPUT_DIR / "extra_unexpected_donation_receipt.pdf",
        "Charitable Donation Receipt",
        [
            "Organization: Goodwill Industries",
            f"Donor: {TAXPAYER}",
            "Donation Value: $340.00",
        ],
    )


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_w2()
    generate_1099_int()
    generate_1099_div()
    generate_1099_nec()
    generate_k1()
    generate_1098()
    generate_prior_year_return()
    generate_ambiguous()
    generate_extra_unexpected()
    print(f"Generated fixtures in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
