from __future__ import annotations
import requests
from typing import Dict, Any
from ..ingest import normalize_record

ZENODO_API = "https://zenodo.org/api/records"

def _map_zenodo_to_internal(obj: Dict[str, Any]) -> Dict[str, Any]:
    md = obj.get("metadata", {})
    creators = [{"name": c.get("name"), "orcid": c.get("orcid"), "email": c.get("affiliation")} for c in md.get("creators", [])]
    access_url = ""
    fmt = ""
    files = obj.get("files") or obj.get("assets",{}).get("files")
    if files:
        f0 = files[0]
        access_url = f0.get("links",{}).get("self") or f0.get("links",{}).get("download") or f0.get("download_url","")
        fmt = (f0.get("type") or f0.get("key","").split(".")[-1]).upper()

    record = {
        "title": md.get("title",""),
        "description": md.get("description",""),
        "keywords": md.get("keywords", []),
        "creators": creators,
        "landing_page": obj.get("links",{}).get("html",""),
        "access_url": access_url,
        "identifier": md.get("doi") or obj.get("doi") or obj.get("conceptdoi") or obj.get("links",{}).get("doi",""),
        "license": (md.get("license") or {}).get("id",""),
        "format": fmt,
        "provenance": md.get("notes",""),
        "version": md.get("version",""),
        "publisher": md.get("journal",{}).get("title") or md.get("publisher","Zenodo"),
        "funder": "", "issued": md.get("publication_date",""), "modified": obj.get("updated",""),
    }
    return normalize_record(record)

def fetch_by_record_id(record_id: int) -> Dict[str, Any]:
    r = requests.get(f"{ZENODO_API}/{record_id}", timeout=30)
    r.raise_for_status()
    return _map_zenodo_to_internal(r.json())

def fetch_by_doi(doi: str) -> Dict[str, Any]:
    params = {"q": f'doi:"{doi}"'}
    r = requests.get(ZENODO_API, params=params, timeout=30)
    r.raise_for_status()
    hits = r.json().get("hits",{}).get("hits",[])
    if not hits:
        raise ValueError(f"Zenodo DOI not found: {doi}")
    return _map_zenodo_to_internal(hits[0])
