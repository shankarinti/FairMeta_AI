# FAIRMeta AI — End‑to‑End App (Realtime + Nice UI)

Multi‑page Streamlit UI with live harvesters (Zenodo/CKAN), batch scoring, report browsing,
side‑by‑side comparison, and an API tester.

## Quickstart
```bash
python -m venv .venv
# Windows:
.\.venv\Scriptsctivate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

# Start the UI
streamlit run ui/Home.py
```

### Pages
- **Harvest**: Zenodo DOI / record id, CKAN slug, or batch CSV → enrich & score → write reports
- **Reports**: Table + bar chart + Markdown report view
- **Compare**: Side‑by‑side charting of two datasets’ F/A/I/R
- **API Tester**: Post custom JSON to `/score` of a running FastAPI server

### Optional: Run the API locally
```bash
uvicorn api.main:app --reload --port 8010
```


## Advanced AI features

The extended version of FAIRMeta AI adds several research‑grade components:

- **Advanced NLP enrichment** (page: *🧠 Advanced Metadata*):
  NER, sentiment and lightweight topic modelling over titles + descriptions.
- **Hybrid recommendation demo** (page: *🎯 Recommendation*):
  TF‑IDF + cosine similarity over enriched metadata, suitable for exploring
  content‑based and hybrid recommendation ideas.
- **Storage & Documentation console** (page: *📦 Storage & Documentation*):
  Explains the on‑disk layout (`data/`, `reports/json`, `reports/md`) so the
  app can be integrated into larger pipelines or cloud storage.
- **Statistics dashboard** (page: *📈 Statistics*):
  Aggregates FAIR scores across all reports and visualises mean F/A/I/R values.

These additions are designed to match the dissertation specification while keeping
the original FAIR scoring behaviour unchanged.
