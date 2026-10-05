"""CNN model for contamination detection placeholder."""
from __future__ import annotations

from typing import Optional


class ContaminationDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model = None

    def load_model(self) -> None:
        self.model = object()

    def predict(self, image_data: bytes) -> dict:
        return {"contaminated": False, "confidence": 0.95}
