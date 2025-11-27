import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import streamlit as st
import pandas as pd
import plotly.express as px

from fairmeta.stats_utils import load_all_scores

st.title("📈 FAIR Statistics Dashboard")

st.markdown(
    """A lightweight analytics view over all FAIR reports generated so far.
    This page gives you **at‑a‑glance statistics** for F/A/I/R scores and can
    act as a mini‑monitoring console for repository curation work."""
)

# Load data
data = load_all_scores()

if not data:
    st.info("No reports found yet. Generate some scores from the Harvest page first.")
else:
    # Prepare DataFrame
    rows = []
    for entry in data:
        row = {"file": entry["file"], "identifier": entry.get("identifier", "")}
        row.update(entry.get("scores", {}))
        rows.append(row)

    df = pd.DataFrame(rows)
    df.columns = df.columns.str.strip()  # Clean up column names

    st.subheader("All Scored Records")
    st.dataframe(df)

    # Show available columns
    st.markdown("#### Debug: Columns in DataFrame")
    st.write(df.columns.tolist())

    expected_cols = ["F", "A", "I", "R", "total"]
    missing_cols = [col for col in expected_cols if col not in df.columns]

    if missing_cols:
        st.warning(f"Missing columns in FAIR report: {missing_cols}")
    else:
        st.subheader("Average FAIR Scores")
        avg = df[expected_cols].mean()
        st.write(avg.to_frame("mean").T)

        fig = px.bar(
            avg.drop(labels=["total"]),
            labels={"index": "Dimension", "value": "Mean score"},
            title="Average FAIR Dimension Scores",
        )
        st.plotly_chart(fig, use_container_width=True)
