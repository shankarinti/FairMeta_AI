import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import streamlit as st
import pandas as pd

from fairmeta.advanced_nlp import enrich_text_advanced
from fairmeta.ingest import normalize_record
from fairmeta.enrich import enrich_record

st.title("🧠 Advanced Metadata Enrichment (NLP)")

st.markdown(
    """Use this page to run **Named Entity Recognition, sentiment analysis and topic
    extraction** over your metadata. This does **not** replace the standard enrichment
    pipeline – it adds an extra `advanced_enrichment` block you can later feed into
    the knowledge‑graph and recommendation modules."""
)

sample = {
    "title": "AI‑Driven Climate Risk Indicators for European Cities",
    "description": "This dataset contains daily climate indicators enriched with AI‑based downscaling models and uncertainty estimates.",
    "keywords": ["climate", "ai", "europe"],
}

col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title", value=sample["title"])
    desc = st.text_area("Description", value=sample["description"], height=160)
with col2:
    st.caption("Optional keywords (comma‑separated)")
    kw_text = st.text_input("Keywords", value=", ".join(sample["keywords"]))
    keywords = [k.strip() for k in kw_text.split(",") if k.strip()]

if st.button("Run advanced enrichment"):
    base_rec = normalize_record(
        {"title": title, "description": desc, "keywords": keywords}
    )
    basic = enrich_record(base_rec)
    adv = enrich_text_advanced(title=title, description=desc)
    basic["advanced_enrichment"] = adv

    st.subheader("Entities")
    ents = adv.get("entities", [])
    if ents:
        st.dataframe(pd.DataFrame(ents))
    else:
        st.info("No entities extracted (spaCy model may not be installed).")

    st.subheader("Sentiment")
    st.metric("Polarity (‑1..1)", f"{adv.get('sentiment', 0.0):.3f}")

    st.subheader("Topics")
    topics = adv.get("topics", [])
    if topics:
        st.write("\n".join(f"• {t}" for t in topics))
    else:
        st.info("Topic modelling not available – install scikit‑learn to enable this.")

    st.subheader("Full enriched record (preview)")
    st.json(basic)
