from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_ROOT / "reports"
REPORTS_JSON = REPORTS_DIR / "json"
REPORTS_MD = REPORTS_DIR / "md"
DATA_DIR = PROJECT_ROOT / "data"

for p in [REPORTS_DIR, REPORTS_JSON, REPORTS_MD, DATA_DIR]:
    p.mkdir(parents=True, exist_ok=True)

CONTROLLED_VOCAB = {
    "machine learning": ["ai", "artificial intelligence", "ml", "neural network", "deep learning"],
    "metadata": ["dublin core", "datacite", "schema.org", "dcat", "ontology"],
    "genomics": ["omics", "rna-seq", "genome", "transcriptomics"],
    "climate": ["meteorology", "weather", "climatology", "temperature", "precipitation"],
    "geospatial": ["gis", "geospatial", "geojson", "geotiff", "coordinates", "crs"],
}

MACHINE_READABLE_FORMATS = {"CSV","JSON","PARQUET","NDJSON","TSV","XML","RDF","TTL","N-TRIPLES","HDF5","NETCDF","GEOJSON"}
OPEN_LICENSES = {"CC-BY","CC-BY-4.0","CC0","ODC-ODbL","ODC-BY","MIT","BSD-3","Apache-2.0","GPL-3.0","GPL-2.0"}
