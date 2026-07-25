# Return Readiness Checker

Drop in the documents a client sent, compare them against what the firm requested, and get an
instant readiness verdict: what's received, what's missing, what needs review, who owns each
follow-up, and a one-click client follow-up draft.

Built as a weekend demo (see `Demo_doc.pdf`) — one client, one readiness check, done well.

## Run it locally

Two terminals:

```bash
# Terminal 1 — backend (FastAPI, port 8000)
cd backend
python -m venv venv
./venv/Scripts/activate        # venv/bin/activate on macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Terminal 2 — frontend (Vite + React, port 5173)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## Try the demo

Synthetic fixture documents live in `data/fixtures/generated/` (regenerate with
`python data/fixtures/generate_fixtures.py` from the repo root, using the backend venv). All
fixtures use a fake client, "Jordan Ellis," matching `data/checklist.json`.

- Upload **all 9 fixtures** → 100% READY (7 checklist items received, 2 extras flagged).
- Upload a **subset** (e.g. skip `k1_riverside_partners.pdf` and `1098_wellsfargo_mortgage.pdf`)
  → NOT READY with the correct missing items, open questions, and owner assignment (K-1 gaps
  route to Partner, other missing items to Client).
- `ambiguous_scan_lowquality.pdf` and `extra_unexpected_donation_receipt.pdf` demonstrate the
  "unreadable" and "not on checklist" paths.

## Architecture

- **Backend** (`backend/app/`): FastAPI. `POST /api/analyze` takes uploaded files, parses text
  (`pypdf`), classifies/extracts fields via an `LLMClient` abstraction, matches results against
  the request checklist, and returns a full `ReadinessReport`. `POST /api/followup-draft`
  generates a client email from that report.
- **LLM layer** (`backend/app/llm/`): `MockLLMClient` classifies documents by filename/keyword
  and extracts fields via regex — no API key needed, runs fully offline. `AnthropicLLMClient` is
  a documented stub for swapping in real Claude calls (structured output for classify+extract,
  vision for scanned docs) once `ANTHROPIC_API_KEY` is available — it's a one-line swap in
  `backend/app/main.py`.
- **Frontend** (`frontend/src/`): React + TypeScript + Vite. No auth, no database — every
  analysis is a single stateless request.

## Scope

Deliberately out of scope for this build: real tax-software/EHR integrations, multi-client
management, auth/accounts, and the heavier prior-year-delta review engine. One client, one
readiness check.
