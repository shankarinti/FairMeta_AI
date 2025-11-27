import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Optional
from fairmeta.ingest import normalize_record
from fairmeta.enrich import enrich_record
from fairmeta.fair_scoring import score_record
from fairmeta.report import write_reports

app = FastAPI(title="FAIRMeta AI", version="1.0.0")

class MetadataIn(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    keywords: Optional[Any] = None
    creators: Optional[Any] = None
    landing_page: Optional[str] = ""
    access_url: Optional[str] = ""
    identifier: Optional[str] = ""
    license: Optional[str] = ""
    format: Optional[str] = ""
    provenance: Optional[str] = ""
    version: Optional[str] = ""
    publisher: Optional[str] = ""
    funder: Optional[str] = ""
    issued: Optional[str] = ""
    modified: Optional[str] = ""

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/score")
def score(md: MetadataIn):
    rec = enrich_record(normalize_record(md.model_dump()))
    result = score_record(rec)
    write_reports(rec, result)
    return {"record": rec, "result": result}
