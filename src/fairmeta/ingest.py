from __future__ import annotations
from pathlib import Path
import csv, json, uuid
from typing import Dict, Any, Iterable

def _normalize_creators(value):
    if value is None:
        return []
    if isinstance(value, list):
        out = []
        for v in value:
            if isinstance(v, dict):
                out.append({"name": v.get("name") or v.get("familyName") or v.get("givenName"),
                            "orcid": v.get("orcid"), "email": v.get("email")})
            else:
                out.append({"name": str(v).strip()})
        return out
    if isinstance(value, str):
        parts = [p.strip() for p in value.split(",") if p.strip()]
        return [{"name": p} for p in parts]
    return [{"name": str(value)}]

def normalize_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    def g(*keys, default=None):
        for k in keys:
            if k in rec and rec[k] not in (None, ""):
                return rec[k]
            for kk in rec:
                if kk.lower() == k.lower() and rec[kk] not in (None, ""):
                    return rec[kk]
        return default

    nid = g("id","identifier","doi","handle","pid","url", default=None)
    record_id = str(uuid.uuid5(uuid.NAMESPACE_URL, str(nid))) if nid else str(uuid.uuid4())

    keywords = g("keywords","tags", default=[])
    if isinstance(keywords, str):
        keywords = [k.strip() for k in keywords.split(",") if k.strip()]
    elif not isinstance(keywords, list):
        keywords = []

    creators = _normalize_creators(g("creators","authors","contributors", default=[]))

    return {
        "record_id": record_id,
        "title": g("title", default=""),
        "description": g("description","abstract", default=""),
        "keywords": keywords,
        "creators": creators,
        "landing_page": g("landing_page","landing","homepage","url", default=""),
        "access_url": g("access_url","download_url","data_url","contentUrl", default=""),
        "identifier": g("identifier","doi","handle","pid","url", default=""),
        "license": g("license","licence","rights", default=""),
        "format": str(g("format","file_format","mediaType", default="")).upper(),
        "provenance": g("provenance","methods","lineage", default=""),
        "version": g("version","version_info","ver", default=""),
        "publisher": g("publisher","organization","organisation", default=""),
        "funder": g("funder","funder_name","funding", default=""),
        "issued": g("issued","publication_date","datePublished", default=""),
        "modified": g("modified","dateModified","updated", default=""),
    }

def read_csv(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            yield normalize_record(row)

def read_jsonl(path: Path) -> Iterable[Dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield normalize_record(json.loads(line))
