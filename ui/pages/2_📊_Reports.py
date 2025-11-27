import sys, pathlib, json, pandas as pd, plotly.express as px
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import streamlit as st
from fairmeta.config import REPORTS_JSON, REPORTS_MD

st.title("Reports")
files = sorted(REPORTS_JSON.glob("*.json"))
if not files:
    st.info("No reports yet. Use the Harvest page first.")
else:
    rows = []
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        rec, sc = data["record"], data["result"]["scores"]
        rows.append({"record_id":rec["record_id"], "title":rec.get("title",""), "id":rec.get("identifier",""),
                     "F":sc["F"], "A":sc["A"], "I":sc["I"], "R":sc["R"], "Total":sc["total"]})
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True)
    st.subheader("Score Distribution")
    fig = px.bar(df.sort_values("Total", ascending=False), x="title", y=["F","A","I","R"], barmode="group")
    st.plotly_chart(fig, use_container_width=True)

    sel = st.selectbox("Open a report", df["record_id"])
    if sel:
        jf = REPORTS_JSON / f"{sel}.json"
        md = REPORTS_MD / f"{sel}.md"
        data = json.loads(jf.read_text(encoding="utf-8"))
        st.markdown(f"### {data['record'].get('title','(no title)')}")
        st.json(data["result"]["scores"])
        st.divider()
        st.markdown(md.read_text(encoding="utf-8"))
