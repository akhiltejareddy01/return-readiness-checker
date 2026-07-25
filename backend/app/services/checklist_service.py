import json
from functools import lru_cache

from app.config import CHECKLIST_PATH
from app.models import RequestChecklist


@lru_cache
def load_checklist() -> RequestChecklist:
    with open(CHECKLIST_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return RequestChecklist.model_validate(data)
