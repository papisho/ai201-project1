"""
Milestone 5 — Streamlit query interface for the Unofficial Guide to CMU Heinz College.

Run with:
    streamlit run app.py
Then open http://localhost:8501
"""

from __future__ import annotations

import streamlit as st

from generate import ask


@st.cache_data(show_spinner=False)
def cached_ask(question: str) -> dict:
    """Cache by question so Streamlit reruns (e.g. opening the expander) don't re-call the API."""
    return ask(question)


st.set_page_config(page_title="Unofficial Guide — CMU Heinz", page_icon="🎓", layout="centered")

st.title("🎓 The Unofficial Guide to CMU Heinz College")
st.caption(
    "Ask about professors and courses. Answers are grounded **only** in student reviews "
    "from RateMyProfessors, Niche, GradReports, and student blogs — every answer lists the "
    "documents it came from. If the reviews don't cover your question, the system says so "
    "instead of guessing."
)

EXAMPLES = [
    "What do students say about Stacy Rosenberg's grading?",
    "How hard is Anand Ramachandran's course 33-658?",
    "Which CS course is recommended for a MISM student who has never coded?",
    "Is Professor Acquisti worth taking?",
]

with st.expander("💡 Example questions"):
    for ex in EXAMPLES:
        st.markdown(f"- {ex}")

question = st.text_input(
    "Your question",
    placeholder="e.g. How is Professor Ramachandran's grading?",
)
asked = st.button("Ask", type="primary")

# Run when the user clicks Ask or presses Enter in the text box (both rerun the script).
if asked or question.strip():
    with st.spinner("Searching the reviews and composing a grounded answer…"):
        result = cached_ask(question)

    st.subheader("Answer")
    st.write(result["answer"])

    if result["sources"]:
        st.subheader("📚 Sources")
        for s in result["sources"]:
            st.markdown(f"- {s}")
    else:
        st.info("No sources cited — the reviews didn't contain enough information to answer.")

    with st.expander("🔍 Retrieved chunks (what the answer was grounded in)"):
        if not result["hits"]:
            st.write("No chunks passed the relevance threshold.")
        for i, h in enumerate(result["hits"], 1):
            st.markdown(
                f"**[{i}] {h['source_file']}**  ·  distance `{h['distance']:.3f}`"
                f"{('  ·  ' + h['review_tag']) if h.get('review_tag') else ''}"
            )
            st.text(h["text"])
