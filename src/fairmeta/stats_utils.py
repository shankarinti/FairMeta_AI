"""Utility helpers for computing summary statistics over FAIR reports."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List
import json

from .config import REPORTS_JSON


def load_all_scores() -> List[Dict[str, Any]]:
    """Load all JSON reports and return their score sections.

    Returns a list of dicts each containing at least:
        { 'id': <identifier>, 'scores': {F,A,I,R,total} }
    """
    scores: List[Dict[str, Any]] = []
    for path in sorted(Path(REPORTS_JSON).glob("*.json")):
        try:
            data = json.loads(path.read_text())
            entry = {
                "file": path.name,
                "identifier": data.get("record", {}).get("identifier", ""),
                "scores": data.get("scores", {}),
            }
            scores.append(entry)
        except Exception:
            continue
    return scores
