from __future__ import annotations
from .config import REPORTS_JSON, REPORTS_MD
from typing import Dict, Any
import json

def write_reports(rec: Dict[str, Any], scoring: Dict[str, Any]) -> None:
    rid = rec.get("record_id","unknown")
    (REPORTS_JSON / f"{rid}.json").write_text(json.dumps({"record":rec, "result":scoring}, indent=2), encoding="utf-8")
    md = []
    md.append(f"# FAIR Report — {rec.get('title','(no title)')}")
    md.append("")
    md.append(f"- **Record ID**: `{rid}`")
    md.append(f"- **Identifier**: `{rec.get('identifier','')}`")
    md.append(f"- **License**: `{rec.get('license','')}`")
    md.append(f"- **Format**: `{rec.get('format','')}`")
    s = scoring["scores"]
    md.append("")
    md.append(f"## Scores")
    md.append(f"- **F**: {s['F']}  |  **A**: {s['A']}  |  **I**: {s['I']}  |  **R**: {s['R']}  |  **Total**: **{s['total']}**")
    md.append("")
    recs = []
    checks = scoring["checks"]
    if not checks["F"]["pid"]: recs.append("Add a persistent identifier (DOI, Handle).")
    if not checks["F"]["keywords"]: recs.append("Provide ≥3 keywords; align to controlled vocabularies.")
    if not checks["A"]["license_present_and_open"]: recs.append("Add an open license (e.g., CC-BY-4.0 or CC0).")
    if not checks["A"]["contact_point"]: recs.append("Add a contact email or maintainer info.")
    if not checks["A"]["format_open"]: recs.append("Provide machine-readable/open formats (CSV/JSON/Parquet).")
    if not checks["I"]["vocab_alignment_hint"]: recs.append("Map keywords to common vocabularies (Schema.org/DCAT).")
    if not checks["R"]["provenance"]: recs.append("Document provenance/methods sufficiently.")
    if not checks["R"]["versioning"]: recs.append("Add a version string and changelog.")
    if not checks["R"]["citation_possible"]: recs.append("Include publisher + title + PID for proper citation.")
    if not recs: recs.append("Great job! This record meets most FAIR best practices.")
    (REPORTS_MD / f"{rid}.md").write_text("\n".join(md), encoding="utf-8")
