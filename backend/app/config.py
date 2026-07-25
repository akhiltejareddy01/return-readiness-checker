from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
REPO_ROOT = BACKEND_DIR.parent
DATA_DIR = REPO_ROOT / "data"
CHECKLIST_PATH = DATA_DIR / "checklist.json"

CORS_ORIGINS = ["http://localhost:5173"]
