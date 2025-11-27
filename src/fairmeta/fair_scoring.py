from __future__ import annotations
from typing import Dict, Any
from .config import MACHINE_READABLE_FORMATS, OPEN_LICENSES

def _has_pid(rec): ident = (rec.get("identifier") or "").lower(); return ident.startswith("10.") or ident.startswith("hdl:") or ident.startswith("http")
def _has_keywords(rec): kws = rec.get("enrichment",{}).get("keyword_union") or rec.get("keywords") or []; return len(kws) >= 3
def _has_landing(rec): return bool(rec.get("landing_page"))
def _has_access(rec): return bool(rec.get("access_url"))
def _has_open_license(rec): lic = (rec.get("license") or "").upper(); return any(ol in lic for ol in OPEN_LICENSES)
def _has_contact(rec): emails = rec.get("enrichment",{}).get("detected_emails", []); return len(emails)>0
def _is_machine_readable(rec): fmt = (rec.get("format") or "").upper(); return fmt in MACHINE_READABLE_FORMATS
def _uses_identifiers(rec): return _has_pid(rec)
def _has_provenance(rec): return len(rec.get("provenance","").strip()) >= 30
def _has_version(rec): return bool(rec.get("version"))

def score_record(rec: Dict[str, Any]) -> Dict[str, Any]:
    F = {"pid":_has_pid(rec), "keywords":_has_keywords(rec), "landing_page":_has_landing(rec), "machine_readable_metadata":True}
    A = {"access_url":_has_access(rec), "license_present_and_open":_has_open_license(rec), "contact_point":_has_contact(rec), "format_open":_is_machine_readable(rec)}
    I = {"uses_identifiers":_uses_identifiers(rec), "machine_readable_format":_is_machine_readable(rec), "vocab_alignment_hint": len(rec.get("enrichment",{}).get("canonical_subjects",[]))>0}
    R = {"clear_license":_has_open_license(rec), "provenance":_has_provenance(rec), "versioning":_has_version(rec), "citation_possible": _has_pid(rec) and bool(rec.get("title")) and bool(rec.get("publisher"))}
    avg = lambda d: sum(1.0 if v else 0.0 for v in d.values())/max(len(d),1)
    scores = {"F":round(avg(F),3), "A":round(avg(A),3), "I":round(avg(I),3), "R":round(avg(R),3)}
    scores["total"] = round((scores["F"]+scores["A"]+scores["I"]+scores["R"])/4.0,3)
    return {"scores":scores, "checks":{"F":F,"A":A,"I":I,"R":R}}
