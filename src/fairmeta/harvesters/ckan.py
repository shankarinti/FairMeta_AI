from __future__ import annotations
import requests
from typing import Dict, Any
from ..ingest import normalize_record

def fetch_ckan_dataset(base_url: str, dataset_id: str) -> Dict[str, Any]:
    api = f"{base_url.rstrip('/')}/api/3/action/package_show"
    r = requests.get(api, params={"id": dataset_id}, timeout=30)
    r.raise_for_status()
    res = r.json()
    if not res.get("success"):
        raise ValueError(f"CKAN lookup failed: {res}")
    pkg = res["result"]
    resources = pkg.get("resources",[])
    access_url = resources[0]["url"] if resources else ""
    fmt = (resources[0].get("format") or "").upper() if resources else ""

    creators = [{"name": pkg.get("author") or pkg.get("maintainer"),
                 "email": pkg.get("author_email") or pkg.get("maintainer_email")}]
    record = {
        "title": pkg.get("title",""),
        "description": pkg.get("notes",""),
        "keywords": [t["name"] for t in pkg.get("tags",[]) if t.get("name")],
        "creators": creators,
        "landing_page": f"{base_url.rstrip('/')}/dataset/{pkg.get('name')}",
        "access_url": access_url,
        "identifier": pkg.get("id"),
        "license": pkg.get("license_id") or pkg.get("license_title",""),
        "format": fmt,
        "provenance": pkg.get("metadata_created",""),
        "version": pkg.get("version",""),
        "publisher": pkg.get("organization",{}).get("title") if pkg.get("organization") else "",
        "funder": "",
        "issued": pkg.get("metadata_created",""),
        "modified": pkg.get("metadata_modified",""),
    }
    return normalize_record(record)
