# ICSE Personalized Question Paper Engine

A versioned question-paper system for **ICSE Class X** that creates subject-wise practice papers matched to each student's current performance, chapter mastery and recent mistakes while preserving the official CISCE examination structure in board-style mode.

## Goal

The system is designed to help a student experience measurable progress without making the paper artificially easy. It uses:

- overall score band
- chapter-wise mastery
- recent trend
- error type (concept, recall, application, careless, language/presentation)
- question difficulty and competency tags
- spaced re-testing of previously missed concepts

Supported subject modules:

1. English Language
2. Literature in English
3. Kannada (Second Language)
4. History & Civics
5. Geography
6. Physics
7. Chemistry
8. Biology
9. Mathematics
10. Physical Education

## Performance bands

`1-40`, `40-50`, `50-60`, `60-70`, `70-80`, `80-90`, `90-95`, `95-100`.

The paper generator does **not** compare raw marks from differently difficult papers as though they were identical. It records paper difficulty, chapter coverage and competency mix so improvement can be reported using both raw score and a normalized mastery/progress index.

## Repository structure

```text
config/                     personalization and paper-generation rules
data/
  sources/                  official-source catalogue and paper metadata
  syllabus/                 syllabus maps by subject
  questions/                original/licensed question-bank data
schemas/                    JSON schemas
docs/                       architecture, sourcing and authoring rules
src/icse_paper_engine/      generation engine
examples/                   sample student + sample question bank
tests/                      automated tests
```

## Source policy

CISCE syllabuses, specimen papers and previous examination papers are used as **references and metadata sources**. This repository should not redistribute copyrighted CISCE papers or commercial textbooks in full. Store source URLs, year, paper code, question number, marks, topic/skill tags and a short original/paraphrased question summary. Teacher-created or otherwise licensed questions may be stored in full.

See `docs/SOURCE_AND_COPYRIGHT_POLICY.md`.

## Personalization principle

A student's paper should contain:

- **recovery questions** from weak concepts at an attainable level;
- **core questions** at the student's present working level;
- **next-step questions** one level above current mastery;
- a small number of **stretch questions**.

As mastery improves, the mix shifts from recall/foundation toward application, analysis, interpretation and evaluation. Board-style papers continue to respect the official subject structure.

## Current status

Phase 1 foundation: repository architecture, official-source catalogue, Class X syllabus map, score-band profiles, schemas and a first deterministic Python generator.

Next phases will ingest the official specimen/previous-paper metadata subject by subject and grow a teacher-authored calibrated question bank.
