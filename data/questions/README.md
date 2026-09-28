# Question Data

This directory is for the production question bank.

Recommended layout:

```text
data/questions/
  english-language/
  english-literature/
  kannada/
  history-civics/
  geography/
  physics/
  chemistry/
  biology/
  mathematics/
  physical-education/
```

Each record must conform to `schemas/question.schema.json`.

## Two separate data layers

### 1. Source-question index

For CISCE previous/specimen papers, keep metadata and an independently written `prompt_summary`, not the full copyrighted question by default. These records are evidence for pattern analysis, recurrence, marks and competency mapping.

### 2. Usable question bank

Questions actually rendered into student papers should be teacher-authored, school-owned, licensed or otherwise permitted. They can be inspired by the skills/patterns discovered in the source index, but should be independently written.

## Review status

Before a question becomes production-ready, add workflow tags such as:

- `draft`
- `subject-reviewed`
- `difficulty-reviewed`
- `answer-key-reviewed`
- `production-ready`

Later versions of the engine will enforce these statuses automatically.
