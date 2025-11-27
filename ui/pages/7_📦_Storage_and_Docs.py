import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

import streamlit as st
from fairmeta.config import PROJECT_ROOT, DATA_DIR, REPORTS_DIR, REPORTS_JSON, REPORTS_MD

st.title("📦 Storage & Documentation")

st.markdown(
    """This page documents **where FAIRMeta AI stores your data on disk** and how
    to work with it. The layout is intentionally similar to a cloud console view,
    with clearly separated sections for *data*, *reports* and *configuration*.
    """
)

st.subheader("Project layout")
st.code(f"""PROJECT_ROOT = {PROJECT_ROOT}
data/            → raw & demo catalogues (CSV, JSON)
reports/json/    → machine‑readable FAIR + enrichment reports
reports/md/      → human‑friendly Markdown reports
api/             → FastAPI service (POST /score)
ui/              → Streamlit console
""")

st.subheader("Directories")
cols = st.columns(3)
with cols[0]:
    st.markdown("**DATA_DIR**")
    st.write(DATA_DIR)
with cols[1]:
    st.markdown("**REPORTS_JSON**")
    st.write(REPORTS_JSON)
with cols[2]:
    st.markdown("**REPORTS_MD**")
    st.write(REPORTS_MD)

st.subheader("Usage tips")
st.markdown(
    """* To add your own catalogue, drop a CSV into `data/` and point the
    *Harvest* or *Recommendation* pages at it.  
    * JSON reports under `reports/json` can be indexed by external search
    engines or harvested into a graph database.  
    * Markdown reports under `reports/md` are ideal for human‑readable
    documentation, data‑management plans, or repository uploads."""
)
