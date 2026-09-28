"""Progress metrics for personalized ICSE practice.

The module intentionally keeps raw marks and challenge indicators separate. It does
not inflate a student's score to manufacture apparent improvement.
"""

from __future__ import annotations

from collections import defaultdict
from statistics import mean
from typing import Any, Dict, Iterable


DIFFICULTY_WEIGHT = {
    "foundation": 0.25,
    "standard": 0.50,
    "application": 0.75,
    "stretch": 1.00,
}

HIGHER_ORDER = {"application", "analysis", "interpretation", "evaluation", "creation"}


def paper_challenge_index(questions: Iterable[Dict[str, Any]]) -> float:
    """Return a transparent 0-100 challenge indicator based on mark-weighted difficulty."""
    questions = list(questions)
    total_marks = sum(float(q.get("marks", 0)) for q in questions)
    if total_marks <= 0:
        return 0.0
    weighted = sum(
        float(q.get("marks", 0)) * DIFFICULTY_WEIGHT.get(q.get("difficulty", "standard"), 0.5)
        for q in questions
    )
    return round(weighted / total_marks * 100, 1)


def higher_order_mark_share(questions: Iterable[Dict[str, Any]]) -> float:
    questions = list(questions)
    total_marks = sum(float(q.get("marks", 0)) for q in questions)
    if total_marks <= 0:
        return 0.0
    higher = sum(
        float(q.get("marks", 0))
        for q in questions
        if q.get("competency") in HIGHER_ORDER
    )
    return round(higher / total_marks * 100, 1)


def score_attempt(attempt: Dict[str, Any]) -> Dict[str, float]:
    awarded = sum(float(r.get("marks_awarded", 0)) for r in attempt.get("responses", []))
    maximum = sum(float(r.get("max_marks", 0)) for r in attempt.get("responses", []))
    percent = (awarded / maximum * 100) if maximum else 0.0
    return {
        "marks_awarded": round(awarded, 2),
        "max_marks": round(maximum, 2),
        "percentage": round(percent, 2),
    }


def evidence_by_chapter(
    attempt: Dict[str, Any],
    questions: Iterable[Dict[str, Any]],
) -> Dict[str, Dict[str, float]]:
    question_map = {q["id"]: q for q in questions}
    awarded = defaultdict(float)
    maximum = defaultdict(float)
    for response in attempt.get("responses", []):
        q = question_map.get(response.get("question_id"))
        if not q:
            continue
        chapter = q["chapter"]
        awarded[chapter] += float(response.get("marks_awarded", 0))
        maximum[chapter] += float(response.get("max_marks", q.get("marks", 0)))

    result: Dict[str, Dict[str, float]] = {}
    for chapter in maximum:
        pct = awarded[chapter] / maximum[chapter] * 100 if maximum[chapter] else 0.0
        result[chapter] = {
            "marks_awarded": round(awarded[chapter], 2),
            "max_marks": round(maximum[chapter], 2),
            "evidence_score": round(pct, 2),
        }
    return result


def update_chapter_mastery(
    old_mastery: Dict[str, float],
    chapter_evidence: Dict[str, Dict[str, float]],
    learning_rate: float = 0.25,
) -> Dict[str, float]:
    """Update mastery with a conservative exponential moving average."""
    if not 0 < learning_rate <= 1:
        raise ValueError("learning_rate must be in (0, 1]")

    updated = {k: float(v) for k, v in old_mastery.items()}
    for chapter, evidence in chapter_evidence.items():
        old = float(updated.get(chapter, 50.0))
        observed = float(evidence["evidence_score"])
        updated[chapter] = round(old * (1 - learning_rate) + observed * learning_rate, 2)
    return updated


def error_counts(attempt: Dict[str, Any]) -> Dict[str, int]:
    counts: Dict[str, int] = defaultdict(int)
    for response in attempt.get("responses", []):
        for tag in response.get("error_tags", []):
            counts[tag] += 1
    return dict(counts)


def progress_report(
    previous_profile: Dict[str, Any],
    attempt: Dict[str, Any],
    paper_questions: Iterable[Dict[str, Any]],
    learning_rate: float = 0.25,
) -> Dict[str, Any]:
    questions = list(paper_questions)
    score = score_attempt(attempt)
    evidence = evidence_by_chapter(attempt, questions)
    old_mastery = previous_profile.get("chapter_mastery", {})
    new_mastery = update_chapter_mastery(old_mastery, evidence, learning_rate=learning_rate)

    chapter_changes = {}
    for chapter in evidence:
        before = float(old_mastery.get(chapter, 50.0))
        after = float(new_mastery[chapter])
        chapter_changes[chapter] = {
            "before": round(before, 2),
            "after": round(after, 2),
            "delta": round(after - before, 2),
        }

    tested_before = [float(old_mastery.get(ch, 50.0)) for ch in evidence]
    tested_after = [float(new_mastery[ch]) for ch in evidence]

    return {
        "student_id": previous_profile.get("student_id"),
        "subject": previous_profile.get("subject"),
        "raw_score": score,
        "paper_challenge_index": paper_challenge_index(questions),
        "higher_order_mark_share": higher_order_mark_share(questions),
        "tested_chapter_mastery_before": round(mean(tested_before), 2) if tested_before else None,
        "tested_chapter_mastery_after": round(mean(tested_after), 2) if tested_after else None,
        "chapter_changes": chapter_changes,
        "error_counts": error_counts(attempt),
        "updated_chapter_mastery": new_mastery,
        "interpretation_note": "Raw marks, challenge and mastery are reported separately; no score inflation is applied."
    }
