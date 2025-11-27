import sys, pathlib, json
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import streamlit as st
import pandas as pd

from fairmeta.ingest import normalize_record
from fairmeta.enrich import enrich_record
from fairmeta.advanced_nlp import enrich_text_advanced
from fairmeta.recommendation import HybridRecommender
from fairmeta.config import DATA_DIR

st.title("🎯 Hybrid Recommendation Demo")

st.markdown(
    """This page demonstrates **hybrid, metadata‑aware recommendations** using the
    enriched records. It combines title, description, keywords and advanced topics
    into a TF‑IDF representation and ranks similar items with cosine similarity."""
)

sample_path = DATA_DIR / "sample_metadata.csv"
if not sample_path.exists():
    st.error(f"Sample metadata CSV not found at {sample_path}")
else:
    df_raw = pd.read_csv(sample_path)
    st.caption("Loaded sample catalogue from `data/sample_metadata.csv`.")
    st.dataframe(df_raw.head())

    # Build enriched records
    records = []
    for _, row in df_raw.iterrows():
        rec = normalize_record(row.to_dict())
        rec = enrich_record(rec)
        rec["advanced_enrichment"] = enrich_text_advanced(
            title=rec.get("title",""),
            description=rec.get("description",""),
        )
        records.append(rec)

    hr = HybridRecommender(records).fit()

    mode = st.radio("Recommend by", ["Free‑text query", "Existing item"], horizontal=True)

    if mode == "Free‑text query":
        query = st.text_input(
            "Describe what you are looking for",
            value="climate risk indicators for european cities",
        )
        k = st.slider("Top‑K", 3, 15, 5)
        if st.button("Recommend"):
            recs = hr.recommend_for_query(query, k=k)
            if not recs:
                st.warning("Recommendation backend not available (install scikit‑learn).")
            else:
                out_rows = []
                for idx, score in recs:
                    r = records[idx]
                    out_rows.append(
                        {
                            "title": r.get("title",""),
                            "identifier": r.get("identifier",""),
                            "score": score,
                            "keywords": ", ".join(r.get("keywords") or []),
                        }
                    )
                st.subheader("Top recommendations")
                st.dataframe(pd.DataFrame(out_rows))
    else:
        options = {f"{i}: {r.get('title','')[:60]}": i for i, r in enumerate(records)}
        label = st.selectbox("Pick a source item", list(options.keys()))
        idx = options[label]
        k = st.slider("Top‑K", 3, 15, 5, key="k_idx")
        if st.button("Find similar items"):
            recs = hr.recommend_for_index(idx, k=k)
            if not recs:
                st.warning("Recommendation backend not available (install scikit‑learn).")
            else:
                out_rows = []
                src = records[idx]
                st.write("**Source item**")
                st.json({"title": src.get("title",""), "keywords": src.get("keywords")})
                for j, score in recs:
                    r = records[j]
                    out_rows.append(
                        {
                            "title": r.get("title",""),
                            "identifier": r.get("identifier",""),
                            "score": score,
                            "keywords": ", ".join(r.get("keywords") or []),
                        }
                    )
                st.subheader("Similar items")
                st.dataframe(pd.DataFrame(out_rows))
