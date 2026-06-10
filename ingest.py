"""
Milestone 3 — Document ingestion and chunking pipeline.

Implements the Chunking Strategy from planning.md:
  - Structure-aware "one review = one chunk" splitting (split body on blank-line blocks).
  - Hard cap of ~512 tokens (~2000 chars); oversized blocks fall back to fixed-width
    splitting with ~50-token (~200-char) overlap.
  - Source/rating metadata parsed from each file's header and PREPENDED to every chunk's
    text, so each chunk is self-contained and carries its citation.

Run directly to load, chunk, validate, and write chunks.json:
    python ingest.py
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path

DOCS_DIR = Path(__file__).parent / "documents"
OUTPUT_FILE = Path(__file__).parent / "chunks.json"

# Plan: ~512-token cap ≈ 2000 chars; ~50-token overlap ≈ 200 chars on fallback splits only.
MAX_CHARS = 2000
OVERLAP_CHARS = 200

# Header keys we care about (everything before the `---` separator line).
RATING_KEYS = {
    "OVERALL_QUALITY": "overall_quality",
    "DIFFICULTY": "difficulty",
    "WOULD_TAKE_AGAIN": "would_take_again",
    "SUMMARY_STATS": "summary_stats",
}

# Matches a review's own leading tag, e.g. "[Course 67262 | Apr 20, 2023 | Quality 5.0 | ...]"
BLOCK_TAG_RE = re.compile(r"^\[(?P<tag>[^\]]+)\]\s*")


@dataclass
class Chunk:
    id: str
    text: str          # metadata-prefixed, self-contained text that gets embedded
    raw_text: str      # the original block text without the prepended header
    metadata: dict = field(default_factory=dict)


def parse_header(raw: str) -> tuple[dict, str]:
    """Split a document into (header_metadata, body). Header ends at the first '---' line."""
    lines = raw.splitlines()
    header_lines: list[str] = []
    body_start = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            body_start = i + 1
            break
        header_lines.append(line)

    meta: dict = {}
    for line in header_lines:
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if key == "SOURCE":
            meta["source"] = value
        elif key == "URL":
            meta["url"] = value
        elif key == "TYPE":
            meta["doc_type"] = value
        elif key == "COLLECTED":
            meta["collected"] = value
        elif key in RATING_KEYS:
            meta[RATING_KEYS[key]] = value
        # NOTE: and any other header lines are intentionally ignored.

    body = "\n".join(lines[body_start:]).strip()
    return meta, body


def clean_text(text: str) -> str:
    """Normalize whitespace and decode the few HTML entities that could appear in copied text."""
    replacements = {
        "&amp;": "&", "&nbsp;": " ", "&#39;": "'", "&quot;": '"',
        "&lt;": "<", "&gt;": ">", " ": " ",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    # Strip any stray HTML tags (defensive — our .txt files shouldn't have them).
    text = re.sub(r"<[^>]+>", "", text)
    # Collapse runs of spaces/tabs but preserve newlines (block structure matters).
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def split_blocks(body: str) -> list[str]:
    """Split a document body into blocks on one-or-more blank lines (one opinion per block)."""
    blocks = re.split(r"\n\s*\n", body)
    return [b.strip() for b in blocks if b.strip()]


def fallback_split(block: str, max_chars: int = MAX_CHARS, overlap: int = OVERLAP_CHARS) -> list[str]:
    """Fixed-width split with overlap, used only for blocks longer than the cap.

    Tries to break on a sentence/space boundary near the cap instead of mid-word.
    """
    if len(block) <= max_chars:
        return [block]

    pieces: list[str] = []
    start = 0
    n = len(block)
    while start < n:
        end = min(start + max_chars, n)
        if end < n:
            window = block[start:end]
            # Prefer to break at the last sentence end, else last space, within the window.
            cut = max(window.rfind(". "), window.rfind("\n"))
            if cut < max_chars * 0.5:  # no good sentence break -> fall back to last space
                cut = window.rfind(" ")
            if cut > 0:
                end = start + cut + 1
        pieces.append(block[start:end].strip())
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return [p for p in pieces if p]


def build_prefix(meta: dict, block_tag: str | None) -> str:
    """Compact, human-readable source/rating header prepended to each chunk."""
    parts = [f"Source: {meta.get('source', meta.get('source_file', 'unknown'))}"]
    if meta.get("doc_type"):
        parts.append(f"Type: {meta['doc_type']}")
    if meta.get("overall_quality"):
        parts.append(f"Overall quality: {meta['overall_quality']}")
    if meta.get("difficulty"):
        parts.append(f"Difficulty: {meta['difficulty']}")
    if meta.get("would_take_again"):
        parts.append(f"Would take again: {meta['would_take_again']}")
    if block_tag:
        parts.append(f"Review: {block_tag}")
    return "[" + " | ".join(parts) + "]"


def load_documents(docs_dir: Path = DOCS_DIR) -> list[dict]:
    """Load every .txt file, parse its header, and clean its body."""
    documents = []
    for path in sorted(docs_dir.glob("*.txt")):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_header(raw)
        meta["source_file"] = path.name
        documents.append({"meta": meta, "body": clean_text(body)})
    return documents


def chunk_documents(documents: list[dict]) -> list[Chunk]:
    """Turn loaded documents into self-contained, metadata-prefixed chunks."""
    chunks: list[Chunk] = []
    for doc in documents:
        meta = doc["meta"]
        stem = Path(meta["source_file"]).stem
        for block in split_blocks(doc["body"]):
            # Extract the review's own leading tag (if any) into metadata + the prefix,
            # and strip it from the body so it isn't duplicated inside the chunk text.
            tag_match = BLOCK_TAG_RE.match(block)
            block_tag = tag_match.group("tag").strip() if tag_match else None
            block_body = block[tag_match.end():].strip() if tag_match else block

            for piece in fallback_split(block_body):
                if not piece:
                    continue
                idx = len(chunks)
                chunk_meta = {
                    "source_file": meta["source_file"],
                    "source": meta.get("source", ""),
                    "url": meta.get("url", ""),
                    "doc_type": meta.get("doc_type", ""),
                    "overall_quality": meta.get("overall_quality"),
                    "difficulty": meta.get("difficulty"),
                    "would_take_again": meta.get("would_take_again"),
                    "review_tag": block_tag,
                }
                prefix = build_prefix({**chunk_meta, **meta}, block_tag)
                chunks.append(
                    Chunk(
                        id=f"{stem}__{idx}",
                        text=f"{prefix}\n{piece}",
                        raw_text=piece,
                        metadata=chunk_meta,
                    )
                )
    return chunks


def main() -> None:
    documents = load_documents()
    chunks = chunk_documents(documents)

    # --- Validation report -------------------------------------------------
    print(f"Loaded {len(documents)} documents from {DOCS_DIR}")
    print(f"Produced {len(chunks)} chunks\n")

    # Per-file chunk counts.
    counts: dict[str, int] = {}
    for c in chunks:
        counts[c.metadata["source_file"]] = counts.get(c.metadata["source_file"], 0) + 1
    print("Chunks per document:")
    for name in sorted(counts):
        print(f"  {counts[name]:>3}  {name}")

    # Length stats — catch fragments and oversized chunks.
    lengths = [len(c.raw_text) for c in chunks]
    empties = sum(1 for n in lengths if n == 0)
    print(f"\nChunk length (raw, chars): min={min(lengths)}  "
          f"max={max(lengths)}  avg={sum(lengths)//len(lengths)}")
    print(f"Empty chunks: {empties}  |  over {MAX_CHARS} chars: {sum(1 for n in lengths if n > MAX_CHARS)}")

    # 5 representative chunks (spread across the corpus).
    print("\n" + "=" * 70)
    print("5 REPRESENTATIVE CHUNKS (inspect: is each self-contained?)")
    print("=" * 70)
    step = max(1, len(chunks) // 5)
    for c in chunks[::step][:5]:
        print(f"\n--- {c.id}  ({len(c.raw_text)} chars, source={c.metadata['source_file']}) ---")
        print(c.text)

    # Persist for Milestone 4.
    OUTPUT_FILE.write_text(
        json.dumps([asdict(c) for c in chunks], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {len(chunks)} chunks to {OUTPUT_FILE.name}")


if __name__ == "__main__":
    main()
