from __future__ import annotations
import re
from typing import Dict, Any
from .config import CONTROLLED_VOCAB

DOI_RX = re.compile(r"(10\.\d{4,9}/[-._;()/:A-Za-z0-9]+)")
HANDLE_RX = re.compile(r"(?:hdl:)?\d{4,5}/[A-Za-z0-9.\-_/]+")
URL_RX = re.compile(r"https?://[^\s]+")
EMAIL_RX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

def enrich_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    text_blob = " ".join([str(rec.get("title","")), str(rec.get("description","")), " ".join(rec.get("keywords",[]))])
    dois = DOI_RX.findall(text_blob) or DOI_RX.findall(rec.get("identifier","") or "")
    handles = HANDLE_RX.findall(text_blob)
    urls = URL_RX.findall(text_blob) + URL_RX.findall(rec.get("landing_page","")) + URL_RX.findall(rec.get("access_url",""))
    emails = EMAIL_RX.findall(text_blob)
    for c in rec.get("creators", []):
        if c.get("email"): emails.append(c["email"])

    suggested = set()
    lower_text = text_blob.lower()
    for canonical, aliases in CONTROLLED_VOCAB.items():
        if canonical in lower_text or any(a in lower_text for a in aliases):
            suggested.add(canonical)

    if not rec.get("identifier") and dois:
        rec["identifier"] = dois[0]
    if not rec.get("landing_page") and rec.get("identifier","").startswith("10."):
        rec["landing_page"] = f"https://doi.org/{rec['identifier']}"

    rec.setdefault("enrichment", {}).update({
        "detected_dois": list(dict.fromkeys(dois)),
        "detected_handles": list(dict.fromkeys(handles)),
        "detected_urls": list(dict.fromkeys(urls)),
        "detected_emails": list(dict.fromkeys(emails)),
        "suggested_keywords": sorted(suggested),
        "keyword_union": sorted(set([*rec.get("keywords",[]), *suggested])),
        "canonical_subjects": sorted(suggested),
    })
    return rec
