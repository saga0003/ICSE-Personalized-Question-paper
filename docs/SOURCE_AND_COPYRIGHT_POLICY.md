# Source and Copyright Policy

## Purpose

This repository may use CISCE syllabuses, specimen papers and previous examination papers to learn the official structure and to build a **question metadata index**. It should not become an unauthorized mirror of copyrighted exam papers or commercial textbooks.

## Safe to store

For an official/published source question, store:

- source title and URL;
- exam year and paper code;
- question number/subpart;
- marks;
- chapter/topic/subtopic;
- competency and difficulty tags;
- answer type;
- whether a map/diagram/extract is involved;
- a short, independently written/paraphrased summary of what the question tests;
- teacher notes and derived analytics.

Teacher-authored, school-owned, licensed or public-domain material may be stored in full if the school has the rights to do so.

## Do not commit by default

- full PDFs of CISCE papers;
- large verbatim copies of CISCE question papers;
- scans/PDFs of commercial textbooks;
- answer keys or guidebooks copied from publishers;
- copyrighted literary works beyond what is needed for metadata/reference.

Instead, keep a link to the legitimate source or a school-controlled private storage location.

## Literature subjects

The bank should mostly contain **original questions about the prescribed text**, not reproduced pages from the work. Extract-based questions should use only material the school is permitted to reproduce and should track the source/license.

## Previous-paper ingestion

When indexing a CISCE question, use `origin.kind = "cisce-metadata"` and normally leave `prompt` empty. Put a concise original description in `prompt_summary`.

Example:

```json
{
  "id": "icse-2025-physics-q3b",
  "subject": "physics",
  "chapter": "Light",
  "marks": 3,
  "difficulty": "application",
  "competency": "application",
  "prompt_summary": "Ray-diagram problem requiring image characteristics for a lens/mirror setup.",
  "origin": {
    "kind": "cisce-metadata",
    "year": 2025,
    "question_number": "3(b)",
    "source_url": "<official CISCE URL>",
    "verbatim_allowed": false
  }
}
```

## Teacher review

Every imported metadata record should be reviewed for:

1. syllabus alignment;
2. correct marks and question type;
3. accurate topic/competency tagging;
4. whether a similar teacher-authored question should be added to the usable bank;
5. copyright/source compliance.
