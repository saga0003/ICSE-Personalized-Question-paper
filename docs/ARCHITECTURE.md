# Architecture

## 1. What the engine personalizes

The engine personalizes **question selection**, not the official board rules. In `board_style=true`, duration, marks, compulsory/choice structure and subject-specific sections must follow the CISCE pattern stored for that subject.

For chapter tests, the school may choose a smaller marks/time blueprint, but every generated paper still records difficulty and competency mix.

## 2. Student model

Each student-subject profile stores:

- current overall score;
- recent score trend;
- chapter and topic mastery;
- error profile: concept, recall, application, careless, presentation/language and time-management errors;
- recently attempted questions;
- missed questions/concepts due for spaced re-testing.

A single percentage is not enough. A student scoring 68% because of one weak chapter needs a different paper from a student scoring 68% evenly across all chapters.

## 3. Question model

Every question is tagged by:

- subject > chapter > topic > subtopic;
- marks and estimated time;
- difficulty: `foundation`, `standard`, `application`, `stretch`;
- competency: recall, understanding, application, analysis, interpretation, evaluation or creation;
- answer type;
- common errors and prerequisites;
- source/licensing metadata;
- later, empirical calibration such as facility, discrimination and average time.

## 4. Personalization algorithm

1. Determine the student's score band.
2. Rank chapters by mastery, recency and error severity.
3. Reserve recovery coverage for weak chapters.
4. Apply the band's target difficulty mix.
5. Add spaced-retrieval items for previously missed concepts.
6. Fill the remaining marks with current-level and next-step questions.
7. Avoid exact recent repeats unless the question is intentionally scheduled for re-testing.
8. Validate subject blueprint, marks, chapter coverage and time estimate.
9. Save a `paper_manifest` containing the exact generator version, question IDs, difficulty mix and random seed.

## 5. Motivation without fake improvement

The system should make progress visible, but must not manufacture improvement by silently making every next paper easier.

Use three reporting layers:

- **Raw score**: what the student scored on this paper.
- **Mastery movement**: chapter/topic mastery before vs after the test.
- **Challenge-adjusted progress**: score interpreted alongside paper difficulty and competency mix.

A student can therefore see messages such as: "Quadratic Equations improved from 54 to 68 mastery; application questions improved from 2/5 to 4/5" even if the total mark moves only slightly.

## 6. Difficulty strategy by band

The mixes live in `config/score_bands.json`. Lower bands get more foundation/recovery questions; higher bands progressively receive more application and stretch questions. No band should receive only easy questions.

For the strongest students, the differentiator is not obscure trivia. Prefer multi-step reasoning, unfamiliar contexts, interpretation, proof/reasoning, precise language and time pressure appropriate to the ICSE pattern.

## 7. Full-syllabus mode

Full-syllabus papers should use the official paper structure and a syllabus coverage matrix. A student's weaker chapters can receive a greater share **only where the official blueprint permits**. The engine must not distort compulsory sections or choice rules.

## 8. Comparison across tests

Never claim a student improved solely because 74% > 70% if the two papers had different difficulty. Store per-paper:

- average question difficulty;
- percentage of marks from application/analysis/interpretation/evaluation;
- chapter coverage;
- expected score band based on calibrated questions;
- time utilization.

Once enough attempt data exists, replace hand-set difficulty with empirical calibration.

## 9. Data pipeline

`Official CISCE source -> paper/question metadata index -> teacher review -> question authoring/calibration -> validated bank -> personalized generator -> student attempt -> analytics -> updated mastery -> next paper`

## 10. Planned modules

- source indexer and reviewer queue;
- teacher question-authoring UI;
- paper generator;
- PDF/DOCX renderer;
- answer key and marking scheme generator;
- student attempt importer;
- chapter-mastery dashboard;
- parent progress report;
- item analysis and difficulty recalibration;
- duplicate/similarity detection so the same concepts are not overused.
