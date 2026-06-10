"""
Milestone 4 — Embedding and retrieval.

Loads the chunks produced by ingest.py, embeds them with all-MiniLM-L6-v2, stores them in a
persistent ChromaDB collection with source metadata, and exposes retrieve() for semantic search.

Usage:
    python vectorstore.py --build      # (re)build the ChromaDB collection from chunks.json
    python vectorstore.py --test       # run sample eval queries and print results
    python vectorstore.py              # build if needed, then run the test queries
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).parent
CHUNKS_FILE = ROOT / "chunks.json"
CHROMA_DIR = ROOT / "chroma_db"
COLLECTION_NAME = "cmu_reviews"
EMBED_MODEL = "all-MiniLM-L6-v2"

# Make stdout UTF-8 so em-dashes etc. print on Windows consoles.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

_model: SentenceTransformer | None = None


def get_model() -> SentenceTransformer:
    """Load the embedding model once and reuse it."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def load_chunks() -> list[dict]:
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("chunks.json not found — run `python ingest.py` first.")
    return json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))


def _clean_metadata(meta: dict, position: int) -> dict:
    """ChromaDB rejects None values; coerce to strings and add the chunk's position."""
    out = {"position": position}
    for key, value in meta.items():
        out[key] = "" if value is None else str(value)
    return out


def build_collection() -> chromadb.Collection:
    """Embed all chunks and (re)create the persistent ChromaDB collection."""
    chunks = load_chunks()
    model = get_model()

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    # Fresh build every time so re-runs don't duplicate or leave stale chunks.
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    # Cosine distance matches how MiniLM embeddings are meant to be compared.
    collection = client.create_collection(
        name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"}
    )

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, show_progress_bar=True, normalize_embeddings=True)

    collection.add(
        ids=[c["id"] for c in chunks],
        embeddings=[e.tolist() for e in embeddings],
        documents=[c["raw_text"] for c in chunks],   # store clean text for display
        metadatas=[_clean_metadata(c["metadata"], i) for i, c in enumerate(chunks)],
    )
    print(f"Built collection '{COLLECTION_NAME}' with {collection.count()} chunks "
          f"(model={EMBED_MODEL}, dim=384, distance=cosine).")
    return collection


def get_collection() -> chromadb.Collection:
    """Open the existing collection, building it if it doesn't exist yet."""
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    try:
        col = client.get_collection(COLLECTION_NAME)
        if col.count() == 0:
            return build_collection()
        return col
    except Exception:
        return build_collection()


def retrieve(query: str, k: int = 5) -> list[dict]:
    """Return the top-k chunks for a query as dicts with text, source metadata, and distance."""
    model = get_model()
    collection = get_collection()
    q_emb = model.encode([query], normalize_embeddings=True)[0].tolist()

    res = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for doc, meta, dist in zip(
        res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        hits.append({
            "text": doc,
            "source_file": meta.get("source_file", ""),
            "source": meta.get("source", ""),
            "url": meta.get("url", ""),
            "review_tag": meta.get("review_tag", ""),
            "distance": dist,
            "metadata": meta,
        })
    return hits


# A subset of the planning.md evaluation questions, used to smoke-test retrieval.
TEST_QUERIES = [
    "What do students say about Stacy Rosenberg's grading, and would they take her again?",
    "How hard is Anand Ramachandran's course 33-658 and how is the grading?",
    "What programming course is recommended for a MISM student who has never coded before?",
]


def run_tests(k: int = 5) -> None:
    for q in TEST_QUERIES:
        print("\n" + "=" * 80)
        print(f"QUERY: {q}")
        print("=" * 80)
        for i, hit in enumerate(retrieve(q, k=k), 1):
            print(f"\n[{i}] distance={hit['distance']:.3f}  source={hit['source_file']}"
                  f"  {hit['review_tag']}")
            text = hit["text"]
            print(f"    {text[:280]}{'...' if len(text) > 280 else ''}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build", action="store_true", help="rebuild the collection")
    parser.add_argument("--test", action="store_true", help="run sample queries")
    parser.add_argument("-k", type=int, default=5, help="top-k for test queries")
    args = parser.parse_args()

    if args.build:
        build_collection()
    if args.test or not args.build:
        run_tests(k=args.k)


if __name__ == "__main__":
    main()
