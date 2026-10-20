
import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RUNBOOKS_PATH = PROJECT_ROOT / "data" / "runbooks.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_THRESHOLD = 0.35


class SemanticSearch:
    def __init__(self, threshold=DEFAULT_THRESHOLD):
        self.threshold = threshold
        self.model = SentenceTransformer(MODEL_NAME)

        with open(RUNBOOKS_PATH, "r", encoding="utf-8") as file:
            self.runbooks = json.load(file)

        self.documents = [
            (
                f"Title: {item['title']}. "
                f"Problem: {item['problem']}. "
                f"Possible causes: {', '.join(item['possible_causes'])}. "
                f"Troubleshooting steps: "
                f"{' '.join(item['troubleshooting_steps'])}"
            )
            for item in self.runbooks
        ]

        self.embeddings = self.model.encode(
            self.documents,
            normalize_embeddings=True
        )

    def search(self, query):
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string.")

        query_embedding = self.model.encode(
            query,
            normalize_embeddings=True
        )

        similarities = self.embeddings @ query_embedding
        best_index = int(np.argmax(similarities))
        best_score = float(similarities[best_index])

        if best_score < self.threshold:
            return {
                "found": False,
                "message": "No sufficiently relevant runbook found.",
                "similarity": round(best_score, 3)
            }

        return {
            "found": True,
            "runbook": self.runbooks[best_index],
            "similarity": round(best_score, 3)
        }

