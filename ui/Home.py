import streamlit as st

st.set_page_config(page_title='FAIRMeta AI', layout='wide')
st.title('FAIRMeta AI — End‑to‑End FAIRness & Metadata Enrichment')
st.caption('Harvest real datasets → enrich metadata → score F/A/I/R → view reports → compare improvements.')

st.markdown('''
**What you can do here**
1. **Harvest** from Zenodo (DOI / record id) or CKAN portals.  
2. **Enrich & Score** automatically with clear, actionable recommendations.  
3. **Browse Reports** (JSON + Markdown) and **Compare** datasets side by side.  
4. **API Tester** to score custom JSON payloads.
''')
st.info('Use the left sidebar to switch pages: Harvest, Reports, Compare, API Tester.')
st.markdown('''
---
**Advanced console sections**

- 🧠 *Advanced Metadata*: NER, sentiment & topics over your records  
- 🎯 *Recommendation*: hybrid, metadata‑aware content suggestions  
- 📦 *Storage & Docs*: where everything lives on disk  
- 📈 *Statistics*: FAIR score analytics dashboard
''')
