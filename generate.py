"""
Milestone 5 — Grounded answer generation.

Connects retrieval (vectorstore.retrieve) to Groq's Llama model. The system prompt enforces
grounding: the model must answer ONLY from the retrieved chunks and must decline when the
context is insufficient. Source attribution is guaranteed programmatically — we build the
source list from the actual retrieved chunk metadata, not from whatever the model decides to cite.

Usage:
    python generate.py                      # run a few end-to-end test questions
    python generate.py "your question"      # ask a single question
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from vectorstore import retrieve

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

load_dotenv()

# Groq's recommended free-tier model for this project.
MODEL = "llama-3.3-70b-versatile"
TOP_K = 5
# Chunks above this cosine distance are too weak to trust as grounding context.
MAX_DISTANCE = 0.6

SYSTEM_PROMPT = """You are the Unofficial Guide to CMU Heinz College, a question-answering \
assistant about student reviews of professors and courses.

STRICT GROUNDING RULES — follow all of them:
1. Answer ONLY using the information in the CONTEXT block below. The context is a set of \
student reviews retrieved for this question.
2. Do NOT use any outside or prior knowledge. Even if you know the answer, if it is not \
supported by the context, you do not know it.
3. If the context does not contain enough information to answer, reply with exactly: \
"I don't have enough information on that." and nothing else.
4. Do not invent professors, courses, ratings, or quotes. Only state what the reviews say.
5. When reviews disagree (e.g., some positive and some negative), present both sides rather \
than picking one.
6. Be concise. Attribute claims to the reviews (e.g., "one reviewer says...", "multiple \
reviewers mention...").

The user-facing app appends the exact source documents separately, so focus on a faithful, \
grounded answer."""

USER_TEMPLATE = """CONTEXT (retrieved student reviews):
{context}

QUESTION: {question}

Answer using only the context above. If it is insufficient, say "I don't have enough \
information on that.\""""

_client: Groq | None = None


def get_client() -> Groq:
    global _client
    if _client is None:
        key = os.getenv("GROQ_API_KEY")
        if not key or key == "your_key_here":
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
                "from https://console.groq.com"
            )
        _client = Groq(api_key=key)
    return _client


def format_context(hits: list[dict]) -> str:
    """Render retrieved chunks as a numbered context block the model can cite."""
    blocks = []
    for i, h in enumerate(hits, 1):
        tag = f" — {h['review_tag']}" if h.get("review_tag") else ""
        blocks.append(f"[{i}] (from {h['source_file']}{tag})\n{h['text']}")
    return "\n\n".join(blocks)


def unique_sources(hits: list[dict]) -> list[str]:
    """Distinct source documents, in first-seen order, for programmatic attribution."""
    seen: list[str] = []
    for h in hits:
        label = h["source_file"]
        if h.get("source"):
            label = f"{h['source_file']} — {h['source']}"
        if label not in seen:
            seen.append(label)
    return seen


def ask(question: str, k: int = TOP_K) -> dict:
    """End-to-end: retrieve -> ground -> generate. Returns answer, sources, and the hits."""
    hits = retrieve(question, k=k)
    # Filter out weak matches so a fishing query can't be "grounded" in irrelevant chunks.
    strong = [h for h in hits if h["distance"] <= MAX_DISTANCE]

    if not strong:
        return {
            "answer": "I don't have enough information on that.",
            "sources": [],
            "hits": hits,
            "grounded": False,
        }

    context = format_context(strong)
    client = get_client()
    completion = client.chat.completions.create(
        model=MODEL,
        temperature=0.1,  # low temperature -> stick to the context, less embellishment
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_TEMPLATE.format(context=context, question=question)},
        ],
    )
    answer = completion.choices[0].message.content.strip()

    declined = answer.lower().startswith("i don't have enough information")
    return {
        "answer": answer,
        # Attribution is built from the retrieved chunks, not from the model's text.
        "sources": [] if declined else unique_sources(strong),
        "hits": strong,
        "grounded": not declined,
    }


TEST_QUESTIONS = [
    "What do students say about Stacy Rosenberg's grading, and would they take her again?",
    "How hard is Anand Ramachandran's course 33-658 and how is the grading?",
    # A question the corpus does NOT cover — should be declined.
    "What are the parking and meal-plan options for graduate students at Heinz?",
]


def _print_result(q: str, result: dict) -> None:
    print("\n" + "=" * 80)
    print(f"Q: {q}")
    print("-" * 80)
    print(result["answer"])
    if result["sources"]:
        print("\nSources:")
        for s in result["sources"]:
            print(f"  • {s}")
    else:
        print("\n(No sources — system declined to answer.)")


def main() -> None:
    if len(sys.argv) > 1:
        q = " ".join(sys.argv[1:])
        _print_result(q, ask(q))
        return
    for q in TEST_QUESTIONS:
        _print_result(q, ask(q))


if __name__ == "__main__":
    main()
