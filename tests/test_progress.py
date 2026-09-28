from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from icse_paper_engine import (  # noqa: E402
    higher_order_mark_share,
    paper_challenge_index,
    progress_report,
)


def test_challenge_and_higher_order_metrics():
    questions = [
        {"id":"q1","chapter":"A","marks":2,"difficulty":"foundation","competency":"recall"},
        {"id":"q2","chapter":"A","marks":2,"difficulty":"application","competency":"application"},
        {"id":"q3","chapter":"B","marks":1,"difficulty":"stretch","competency":"analysis"},
    ]
    assert paper_challenge_index(questions) == 60.0
    assert higher_order_mark_share(questions) == 60.0


def test_progress_report_keeps_raw_score_separate():
    profile = {
        "student_id":"s1",
        "subject":"physics",
        "chapter_mastery":{"Electricity and Magnetism":48.0,"Heat":56.0},
    }
    questions = [
        {"id":"q1","chapter":"Electricity and Magnetism","marks":2,"difficulty":"standard","competency":"application"},
        {"id":"q2","chapter":"Heat","marks":3,"difficulty":"application","competency":"analysis"},
    ]
    attempt = {
        "student_id":"s1",
        "subject":"physics",
        "paper_id":"p1",
        "responses":[
            {"question_id":"q1","marks_awarded":2,"max_marks":2,"error_tags":[]},
            {"question_id":"q2","marks_awarded":2,"max_marks":3,"error_tags":["careless"]},
        ],
    }
    report = progress_report(profile, attempt, questions)
    assert report["raw_score"]["percentage"] == 80.0
    assert report["chapter_changes"]["Electricity and Magnetism"]["delta"] > 0
    assert report["error_counts"]["careless"] == 1
    assert "no score inflation" in report["interpretation_note"]
