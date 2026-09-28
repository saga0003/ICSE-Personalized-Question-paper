"""Core deterministic personalized-paper selector.

This module intentionally generates a *manifest* of selected questions. Rendering to
PDF/DOCX and exact subject-section blueprint enforcement are separate layers.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List


DIFFICULTIES = ("foundation", "standard", "application", "stretch")


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def score_band(score: float, bands_config: Dict[str, Any]) -> Dict[str, Any]:
    bands = bands_config["bands"]
    for band in bands:
        if band["min"] <= score <= band["max"]:
            return band
    if score < bands[0]["min"]:
        return bands[0]
    return bands[-1]


def _difficulty_rank(name: str) -> int:
    return DIFFICULTIES.index(name)


def _question_priority(
    question: Dict[str, Any],
    profile: Dict[str, Any],
    desired_difficulty: str,
    rng: random.Random,
) -> float:
    chapter = question["chapter"]
    mastery = profile.get("chapter_mastery", {}).get(chapter, profile.get("overall_score", 50))
    weakness = (100.0 - float(mastery)) / 100.0

    qdiff = question["difficulty"]
    gap = abs(_difficulty_rank(qdiff) - _difficulty_rank(desired_difficulty))
    difficulty_fit = 1.0 - min(gap, 3) * 0.22

    qid = question["id"]
    missed = set(profile.get("missed_question_ids", []))
    recent = set(profile.get("recent_question_ids", []))
    retrieval_bonus = 0.35 if qid in missed else 0.0
    recent_penalty = -0.55 if qid in recent and qid not in missed else 0.0

    calibration = question.get("calibration", {})
    attempts = int(calibration.get("attempts", 0) or 0)
    data_bonus = min(attempts / 100.0, 0.12)

    # Tiny seeded jitter makes ties deterministic for a given seed without making
    # the selection rigid forever.
    jitter = rng.random() * 0.02
    return weakness * 0.48 + difficulty_fit * 0.42 + retrieval_bonus + recent_penalty + data_bonus + jitter


def _quota_marks(target_marks: int, mix: Dict[str, float]) -> Dict[str, int]:
    raw = {d: target_marks * float(mix.get(d, 0)) for d in DIFFICULTIES}
    marks = {d: int(raw[d]) for d in DIFFICULTIES}
    remainder = target_marks - sum(marks.values())
    order = sorted(DIFFICULTIES, key=lambda d: raw[d] - marks[d], reverse=True)
    for d in order[:remainder]:
        marks[d] += 1
    return marks


def generate_manifest(
    profile: Dict[str, Any],
    question_bank: Iterable[Dict[str, Any]],
    bands_config: Dict[str, Any],
    target_marks: int,
    seed: int = 1,
) -> Dict[str, Any]:
    """Select questions for one student and return a reproducible paper manifest.

    The bank is expected to already contain questions allowed for use in generated
    papers (teacher-authored/licensed/school-owned). CISCE metadata-only rows should
    normally not contain a full prompt and therefore are skipped here.
    """
    if target_marks <= 0:
        raise ValueError("target_marks must be positive")

    subject = profile["subject"]
    usable = [
        q for q in question_bank
        if q.get("subject") == subject and (q.get("prompt") or q.get("origin", {}).get("verbatim_allowed"))
    ]
    if not usable:
        raise ValueError(f"No usable full-text questions available for subject: {subject}")

    band = score_band(float(profile.get("overall_score", 0)), bands_config)
    quotas = _quota_marks(target_marks, band["difficulty_mix"])
    rng = random.Random(seed)

    selected: List[Dict[str, Any]] = []
    selected_ids: set[str] = set()
    selected_marks = 0

    for desired in DIFFICULTIES:
        need = quotas[desired]
        candidates = sorted(
            usable,
            key=lambda q: _question_priority(q, profile, desired, rng),
            reverse=True,
        )
        gained = 0
        for q in candidates:
            if q["id"] in selected_ids:
                continue
            marks = int(q["marks"])
            if selected_marks + marks > target_marks:
                continue
            # Prefer the requested difficulty during quota filling. Questions one
            # step away may be used when the bank is still small.
            if abs(_difficulty_rank(q["difficulty"]) - _difficulty_rank(desired)) > 1:
                continue
            selected.append(q)
            selected_ids.add(q["id"])
            selected_marks += marks
            gained += marks
            if gained >= need or selected_marks >= target_marks:
                break

    if selected_marks < target_marks:
        leftovers = sorted(
            (q for q in usable if q["id"] not in selected_ids),
            key=lambda q: _question_priority(q, profile, "standard", rng),
            reverse=True,
        )
        for q in leftovers:
            marks = int(q["marks"])
            if selected_marks + marks <= target_marks:
                selected.append(q)
                selected_ids.add(q["id"])
                selected_marks += marks
            if selected_marks >= target_marks:
                break

    chapter_marks: Dict[str, int] = defaultdict(int)
    difficulty_marks: Dict[str, int] = defaultdict(int)
    competency_marks: Dict[str, int] = defaultdict(int)
    for q in selected:
        marks = int(q["marks"])
        chapter_marks[q["chapter"]] += marks
        difficulty_marks[q["difficulty"]] += marks
        competency_marks[q["competency"]] += marks

    return {
        "engine_version": "0.1.0",
        "student_id": profile.get("student_id"),
        "subject": subject,
        "score_band": band["id"],
        "starting_score": profile.get("overall_score"),
        "target_gain_points": band.get("target_gain_points"),
        "target_marks": target_marks,
        "actual_marks": selected_marks,
        "seed": seed,
        "question_ids": [q["id"] for q in selected],
        "chapter_marks": dict(chapter_marks),
        "difficulty_marks": dict(difficulty_marks),
        "competency_marks": dict(competency_marks),
        "questions": selected,
        "warnings": [] if selected_marks == target_marks else [
            f"Question bank could only fill {selected_marks}/{target_marks} marks exactly. Add more calibrated questions."
        ],
    }
