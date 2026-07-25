from abc import ABC, abstractmethod

from app.models import DocClassification
from app.parsing.extract_text import ParsedDocument


class LLMClient(ABC):
    @abstractmethod
    def classify_and_extract(self, doc: ParsedDocument) -> DocClassification:
        """Classify a document's tax-form type and extract key fields."""
        raise NotImplementedError
