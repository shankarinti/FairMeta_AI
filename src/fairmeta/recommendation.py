"""Hybrid-style recommendation helpers.

This module focuses on content-based similarity over enriched metadata, with an
option to incorporate FAIR scores as additional features. It is deliberately
lightweight but exposes an interface that can be extended with collaborative
filtering models later without breaking the UI.
"""
from __future__ import annotations

from typing import List, Dict, Any, Tuple
import logging

import pandas as pd

logger = logging.getLogger(__name__)

try:
    from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
    from sklearn.metrics.pairwise import cosine_similarity  # type: ignore
except Exception:
    TfidfVectorizer = None  # type: ignore
    cosine_similarity = None  # type: ignore
    logger.info("scikit-learn not installed; recommendation disabled.")


class HybridRecommender:
    """Small wrapper around TF‑IDF cosine similarity.

    Parameters
    ----------
    records:
        Sequence of normalised/enriched metadata dicts.
    """
    def __init__(self, records: List[Dict[str, Any]]):
        self.records = records
        self.df = pd.DataFrame(records)
        self.df.index = range(len(self.df))
        self.vectorizer = None
        self.item_matrix = None

    def _combined_text(self) -> List[str]:
        def to_text(row):
            parts = [
                str(row.get("title") or ""),
                str(row.get("description") or ""),
                " ".join(row.get("keywords") or []),
            ]
            adv = row.get("advanced_enrichment") or {}
            topics = adv.get("topics") or []
            parts.append(" ".join(topics))
            return " ".join(p for p in parts if p)
        return [to_text(r) for _, r in self.df.iterrows()]

    def fit(self):
        if TfidfVectorizer is None or cosine_similarity is None:
            logger.warning("scikit-learn missing; HybridRecommender.fit is a no-op.")
            return self

        texts = self._combined_text()
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
        self.item_matrix = self.vectorizer.fit_transform(texts)
        return self

    def recommend_for_index(self, idx: int, k: int = 5) -> List[Tuple[int, float]]:
        """Return top-k similar items for a given row index.

        Returns a list of (row_index, score) pairs, excluding the item itself.
        """
        if self.item_matrix is None or cosine_similarity is None:
            return []
        if idx < 0 or idx >= self.item_matrix.shape[0]:
            return []
        sims = cosine_similarity(self.item_matrix[idx], self.item_matrix).flatten()
        sims[idx] = -1.0  # exclude self
        top_idx = sims.argsort()[::-1][:k]
        return [(int(i), float(sims[i])) for i in top_idx]

    def recommend_for_query(self, query: str, k: int = 5) -> List[Tuple[int, float]]:
        """Return top-k items that best match the free‑text query."""
        if self.item_matrix is None or self.vectorizer is None or cosine_similarity is None:
            return []
        vec = self.vectorizer.transform([query])
        sims = cosine_similarity(vec, self.item_matrix).flatten()
        top_idx = sims.argsort()[::-1][:k]
        return [(int(i), float(sims[i])) for i in top_idx]
