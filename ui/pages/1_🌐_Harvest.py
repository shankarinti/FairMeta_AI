import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import streamlit as st
from fairmeta.harvesters.zenodo import fetch_by_doi, fetch_by_record_id
from fairmeta.harvesters.ckan import fetch_ckan_dataset
from fairmeta.enrich import enrich_record
from fairmeta.fair_scoring import score_record
from fairmeta.report import write_reports

st.title("Harvest & Score (Realtime)")

tabs = st.tabs(["Zenodo", "CKAN", "Batch CSV"])

with tabs[0]:
    st.subheader("Zenodo by DOI / record id")
    doi = st.text_input("Zenodo DOI (e.g., 10.5281/zenodo.4055214)")
    rid = st.text_input("Zenodo record id (alternative to DOI)", help="Provide either DOI or record id")
    if st.button("Harvest from Zenodo"):
        try:
            rec = fetch_by_doi(doi) if doi else fetch_by_record_id(int(rid))
            rec = enrich_record(rec); result = score_record(rec); write_reports(rec, result)
            st.success("Harvested & Scored ✅")
            st.json(result["scores"])
            st.code(json.dumps(rec, indent=2))
        except Exception as e:
            st.error(f"Zenodo harvest failed: {e}")

with tabs[1]:
    st.subheader("CKAN dataset")
    base = st.text_input("CKAN Base URL", value="https://data.gov.ie")
    slug = st.text_input("Dataset slug", placeholder="e.g., dublin-city-bicycle-counters")
    if st.button("Harvest from CKAN"):
        try:
            rec = fetch_ckan_dataset(base, slug)
            rec = enrich_record(rec); result = score_record(rec); write_reports(rec, result)
            st.success("Harvested & Scored ✅")
            st.json(result["scores"])
            st.code(json.dumps(rec, indent=2))
        except Exception as e:
            st.error(f"CKAN harvest failed: {e}")

with tabs[2]:
    st.subheader("Batch from CSV (local)")
    st.caption("CSV with columns like: title, description, keywords, creators, access_url, identifier, license, format, provenance, version, publisher, issued, modified")
    up = st.file_uploader("Upload CSV", type=["csv"])
    if up and st.button("Run batch"):
        import pandas as pd
        from fairmeta.ingest import read_csv, normalize_record
        from io import StringIO
        buf = StringIO(up.getvalue().decode("utf-8"))
        df = pd.read_csv(buf)
        count = 0
        for _, row in df.iterrows():
            rec = normalize_record(row.to_dict())
            rec = enrich_record(rec); result = score_record(rec); write_reports(rec, result)
            count += 1
        st.success(f"Processed {count} records and wrote reports ✅")
