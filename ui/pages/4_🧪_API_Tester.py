import sys, pathlib, json, requests, streamlit as st
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1] / "src"))

st.title("API Tester")
st.caption("Post a custom metadata JSON to a running FAIRMeta API instance (uvicorn api.main:app).")

url = st.text_input("API URL", value="http://localhost:8010/score")
sample = {
    "title": "EU Climate Daily",
    "description": "Daily temperature + precipitation. DOI:10.1234/abcd.5678",
    "keywords": ["climate","temperature","meteorology"],
    "creators": [{"name":"Alice","email":"alice@example.org"}],
    "identifier": "10.1234/abcd.5678",
    "license": "CC-BY-4.0", "format": "CSV", "publisher":"Open Science Lab",
    "provenance": "Compiled from ERA5/E-OBS; QC outliers; resampled daily; scripts in repo.", "version":"1.2.0"
}
payload = st.text_area("Metadata JSON", value=json.dumps(sample, indent=2), height=240)
if st.button("POST /score"):
    try:
        resp = requests.post(url, json=json.loads(payload))
        st.write("Status:", resp.status_code)
        st.json(resp.json())
    except Exception as e:
        st.error(e)
