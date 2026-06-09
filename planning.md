# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

This Unofficial Guide covers student-written reviews of professors and courses at Carnegie
Mellon's Heinz College (MISM, MSPPM, and MPM tracks) and the cross-listed School of Computer
Science courses that Heinz graduate students take. Official course catalogs list topics and
prerequisites but reveal nothing about teaching style, grading harshness, workload, or whether
a professor's lectures are actually worth attending — exactly what students weigh before they
register. That knowledge lives scattered and anonymized across RateMyProfessors, program-review
sites, and student blogs; this system makes it searchable and answerable, with citations.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | RateMyProfessors | Raja Sooriamurthi (Heinz, Information Systems) — 4 reviews, 4.8/5, positive | `documents/rmp_sooriamurthi.txt` |
| 2 | RateMyProfessors | Stacy Rosenberg (Heinz, Writing/Policy core) — 4 reviews, 1.3/5, very negative | `documents/rmp_rosenberg.txt` |
| 3 | RateMyProfessors | Beibei Li (Heinz, IT Management) — 2 reviews, 2.3/5, negative | `documents/rmp_li.txt` |
| 4 | RateMyProfessors | Alessandro Acquisti (Heinz, Information Systems) — 5 reviews, 4.7/5, positive | `documents/rmp_acquisti.txt` |
| 5 | RateMyProfessors | Anand Ramachandran (SCS, Computer Science) — 5 reviews, 2.3/5, brutal grader | `documents/rmp_ramachandran.txt` |
| 6 | Niche | Heinz College program reviews — 8 MPM/policy student reviews | `documents/niche_heinz.txt` |
| 7 | GradReports | Carnegie Mellon alumni reviews — 20 program reviews | `documents/gradreports_cmu.txt` |
| 8 | Student blog (dalanmiller.com) | MISM grad retrospective — program, workload, career services | `documents/blog_mism_retrospective.txt` |
| 9 | Quora | "Best CS courses for a MISM student" course guide (contains some factual errors — kept intentionally) | `documents/quora_best_cs_courses_mism.txt` |
| 10 | Medium (@plengchanokw) | MISM/BIDA year-in-review — 5 named-professor course reviews | `documents/medium_mism_year_review.txt` |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
