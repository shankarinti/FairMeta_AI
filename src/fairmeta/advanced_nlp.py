"""Advanced NLP-based metadata enrichment utilities.

These functions are *additive* and do not change the behaviour of the existing
`enrich_record` pipeline. They can be used from the UI or other modules to
perform deeper analysis such as NER, sentiment, and simple topic modelling.

The design is defensive: if heavy NLP libraries or models are not installed,
the functions degrade gracefully and return partial results instead of raising
hard errors. This makes the project easier to run in constrained environments
while still aligning with the dissertation specification.
"""
from __future__ import annotations

from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

# --- Optional imports -------------------------------------------------------
try:
    import spacy  # type: ignore
    try:
        _NLP = spacy.load("en_core_web_sm")
    except Exception:  # model not downloaded yet
        _NLP = None
        logger.warning("spaCy model 'en_core_web_sm' is not available. "
                       "Run: python -m spacy download en_core_web_sm")
except Exception:
    spacy = None  # type: ignore
    _NLP = None   # type: ignore
    logger.info("spaCy not installed; NER will be skipped.")

try:
    from textblob import TextBlob  # type: ignore
except Exception:
    TextBlob = None  # type: ignore
    logger.info("TextBlob not installed; sentiment will be rule-based only.")

try:
    from sklearn.feature_extraction.text import CountVectorizer  # type: ignore
    from sklearn.decomposition import LatentDirichletAllocation  # type: ignore
except Exception:
    CountVectorizer = None  # type: ignore
    LatentDirichletAllocation = None  # type: ignore
    logger.info("scikit-learn not fully available; topic modelling disabled.")


def _simple_sentiment(text: str) -> float:
    """Return sentiment polarity in [-1, 1].

    Uses TextBlob when available; otherwise falls back to a trivial lexicon-based
    count of positive vs negative words so the function always returns a value.
    """
    text = text or ""
    if TextBlob is not None:
        try:
            return float(TextBlob(text).sentiment.polarity)
        except Exception:
            pass

    positive = {"good", "great", "excellent", "positive", "useful", "helpful", "robust"}
    negative = {"bad", "poor", "negative", "buggy", "broken", "biased"}
    tokens = {t.strip(".,;:!?()").lower() for t in text.split()}
    score = sum(1 for t in tokens if t in positive) - sum(1 for t in tokens if t in negative)
    if not tokens:
        return 0.0
    # normalise roughly into [-1,1]
    return max(-1.0, min(1.0, score / max(len(tokens), 5)))


def _extract_entities(text: str) -> List[Dict[str, Any]]:
    """Extract named entities using spaCy where available.

    Returns a list of {text, label} dictionaries.
    """
    text = text or ""
    if not text.strip() or _NLP is None:
        return []
    try:
        doc = _NLP(text)
    except Exception as exc:  # pragma: no cover - very environment specific
        logger.warning("spaCy NER failed: %s", exc)
        return []
    ents = []
    for ent in doc.ents:
        ents.append({"text": ent.text, "label": ent.label_})
    return ents


def _topic_labels(texts: List[str], n_topics: int = 3, n_words: int = 5) -> List[str]:
    """Very small LDA topic modeller over a tiny corpus.

    This is mainly illustrative and intended for small demo corpora derived
    from a handful of records or a single user query.
    """
    if CountVectorizer is None or LatentDirichletAllocation is None:
        return []

    docs = [t for t in texts if t]
    if len(docs) < 1:
        return []

    try:
        vectorizer = CountVectorizer(max_features=1000, stop_words="english")
        X = vectorizer.fit_transform(docs)
        lda = LatentDirichletAllocation(
            n_components=min(n_topics, max(1, len(docs))),
            random_state=42,
            learning_method="online",
        )
        lda.fit(X)
        words = vectorizer.get_feature_names_out()
        labels: List[str] = []
        for topic_idx, topic in enumerate(lda.components_):
            top_idx = topic.argsort()[::-1][:n_words]
            label = "Topic %d: %s" % (
                topic_idx + 1,
                ", ".join(words[i] for i in top_idx),
            )
            labels.append(label)
        return labels
    except Exception as exc:  # pragma: no cover
        logger.warning("Topic modelling failed: %s", exc)
        return []


def enrich_text_advanced(title: str = "", description: str = "") -> Dict[str, Any]:
    """High-level enrichment wrapper used by the UI and API.

    Parameters
    ----------
    title, description:
        Core textual fields from a metadata record.

    Returns
    -------
    dict with keys:
        - sentiment: float in [-1,1]
        - entities: list of {text,label}
        - topics: list of topic label strings
    """
    combined = "\n\n".join([t for t in [title or "", description or ""] if t])
    sentiment = _simple_sentiment(combined)
    entities = _extract_entities(combined)
    topics = _topic_labels([combined])

    return {
        "sentiment": sentiment,
        "entities": entities,
        "topics": topics,
    }
