# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This Unofficial Guide covers student-written reviews of professors and courses at Carnegie
Mellon's Heinz College (MISM, MSPPM, and MPM tracks) and the cross-listed School of Computer
Science courses that Heinz graduate students take. Official course catalogs list topics and
prerequisites but reveal nothing about teaching style, grading harshness, workload, or whether
a professor's lectures are actually worth attending — exactly what students weigh before they
register. That knowledge lives scattered and anonymized across RateMyProfessors, program-review
sites, and student blogs; this system makes it searchable and answerable, with citations.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source                                                          | Type             | URL or file path                                                                                                                                      |
| --- | --------------------------------------------------------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | RateMyProfessors — Raja Sooriamurthi (Heinz, IS)                | professor_review | https://www.ratemyprofessors.com/professor/1753353 → `documents/rmp_sooriamurthi.txt`                                                                 |
| 2   | RateMyProfessors — Stacy Rosenberg (Heinz, Writing/Policy core) | professor_review | https://www.ratemyprofessors.com/professor/2146454 → `documents/rmp_rosenberg.txt`                                                                    |
| 3   | RateMyProfessors — Beibei Li (Heinz, IT Management)             | professor_review | https://www.ratemyprofessors.com/professor/1939662 → `documents/rmp_li.txt`                                                                           |
| 4   | RateMyProfessors — Alessandro Acquisti (Heinz, IS)              | professor_review | https://www.ratemyprofessors.com/professor/802198 → `documents/rmp_acquisti.txt`                                                                      |
| 5   | RateMyProfessors — Anand Ramachandran (SCS, CS)                 | professor_review | https://www.ratemyprofessors.com/professor/2814031 → `documents/rmp_ramachandran.txt`                                                                 |
| 6   | Niche — Heinz College reviews                                   | program_review   | https://www.niche.com/graduate-schools/heinz-college-of-information-systems-and-public-policy/reviews/ → `documents/niche_heinz.txt`                  |
| 7   | GradReports — Carnegie Mellon University                        | program_review   | https://www.gradreports.com/colleges/carnegie-mellon-university → `documents/gradreports_cmu.txt`                                                     |
| 8   | Student blog — MISM retrospective                               | student_blog     | https://blog.dalanmiller.com/a-retrospective-as-a-master-of-information-systems-management/ → `documents/blog_mism_retrospective.txt`                 |
| 9   | Quora — best CS courses for MISM                                | forum_thread     | https://www.quora.com/What-are-the-best-CS-courses-at-CMU-for-someone-in-the-Heinz-Colleges-MISM-program → `documents/quora_best_cs_courses_mism.txt` |
| 10  | Medium — MISM/BIDA year in review                               | student_blog     | https://medium.com/@plengchanokw/my-year-in-review-at-carnegie-mellon-mism-bida-d90747766296 → `documents/medium_mism_year_review.txt`                |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | -------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   |          |                 |                              |                   |                   |
| 2   |          |                 |                              |                   |                   |
| 3   |          |                 |                              |                   |                   |
| 4   |          |                 |                              |                   |                   |
| 5   |          |                 |                              |                   |                   |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_

**Instance 2**

- _What I gave the AI:_
- _What it produced:_
- _What I changed or overrode:_
