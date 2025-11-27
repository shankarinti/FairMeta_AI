import sys, pathlib, json, pandas as pd, plotly.express as px
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import streamlit as st
from fairmeta.config import REPORTS_JSON

st.title("Compare Datasets")
files = sorted(REPORTS_JSON.glob("*.json"))
if len(files) < 2:
    st.info("Need at least two reports to compare. Harvest another dataset first.")
else:
    options = []
    store = {}
    for f in files:
        d = json.loads(f.read_text(encoding="utf-8"))
        rec, scores = d["record"], d["result"]["scores"]
        label = f"{rec.get('title','(no title)')} — {rec.get('identifier','')}"
        options.append(label); store[label] = scores
    left = st.selectbox("Left", options, index=0)
    right = st.selectbox("Right", options, index=1 if len(options)>1 else 0)
    l, r = store[left], store[right]
    df = pd.DataFrame([l, r], index=["Left","Right"])
    st.dataframe(df, use_container_width=True)
    fig = px.bar(df.reset_index().melt(id_vars="index", var_name="Metric", value_name="Score"),
                 x="Metric", y="Score", color="index", barmode="group")
    st.plotly_chart(fig, use_container_width=True)
