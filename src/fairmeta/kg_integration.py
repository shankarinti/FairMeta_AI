"""Simple knowledge graph construction utilities.

The goal is to turn enriched metadata into a lightweight RDF graph that can be
exported or queried. This is intentionally minimal but demonstrates how the
framework can integrate with KGs as described in the report.
"""
from __future__ import annotations

from typing import Iterable, Dict, Any
import logging

logger = logging.getLogger(__name__)

try:
    import rdflib  # type: ignore
    from rdflib import Graph, Namespace, URIRef, Literal  # type: ignore
except Exception:
    rdflib = None  # type: ignore
    Graph = None   # type: ignore
    Namespace = None  # type: ignore
    URIRef = None  # type: ignore
    Literal = None  # type: ignore
    logger.info("rdflib not installed; KG construction disabled.")


def build_kg(records: Iterable[Dict[str, Any]]):
    """Build an in-memory RDF graph from a sequence of metadata records.

    Each record is expected to follow the internal normalised schema used by
    `fairmeta.ingest.normalize_record`.
    """
    if Graph is None or Namespace is None:
        return None

    g = Graph()
    EX = Namespace("http://example.org/dataset/")
    META = Namespace("http://example.org/metadata/")

    g.bind("ex", EX)
    g.bind("meta", META)

    for rec in records:
        identifier = rec.get("identifier") or rec.get("title") or "item"
        node = URIRef(EX[str(identifier)])

        title = rec.get("title") or ""
        if title:
            g.add((node, META.title, Literal(title)))

        desc = rec.get("description") or ""
        if desc:
            g.add((node, META.description, Literal(desc)))

        for kw in rec.get("keywords") or []:
            g.add((node, META.keyword, Literal(str(kw))))

        # Optional: attach sentiment/topics if present
        adv = rec.get("advanced_enrichment") or {}
        if adv.get("sentiment") is not None:
            g.add((node, META.sentiment, Literal(float(adv["sentiment"]))))

        for ent in adv.get("entities") or []:
            ent_node = URIRef(EX[f"entity/{ent.get('text','').strip().replace(' ', '_')}"])
            g.add((node, META.hasEntity, ent_node))
            if ent.get("label"):
                g.add((ent_node, META.label, Literal(ent["label"])))

    return g


def export_kg_turtle(graph, path: str):
    """Serialise the KG to a Turtle file.

    If rdflib is missing, this becomes a no-op so callers do not fail.
    """
    if graph is None or rdflib is None:
        logger.warning("No graph available; skipping KG export.")
        return
    try:
        graph.serialize(destination=path, format="turtle")
    except Exception as exc:  # pragma: no cover
        logger.error("Failed to serialise KG: %s", exc)
