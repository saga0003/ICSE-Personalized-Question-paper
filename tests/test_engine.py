from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from icse_paper_engine import generate_manifest, score_band  # noqa: E402


def _load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def test_score_band_boundaries():
    config = _load("config/score_bands.json")
    assert score_band(39, config)["id"] == "1-40"
    assert score_band(40, config)["id"] == "40-50"
    assert score_band(67, config)["id"] == "60-70"
    assert score_band(92, config)["id"] == "90-95"
    assert score_band(99, config)["id"] == "95-100"


def test_generate_manifest_is_reproducible_and_personalized():
    config = _load("config/score_bands.json")
    profile = _load("examples/student_profile.sample.json")
    bank = _load("examples/question_bank.sample.json")

    a = generate_manifest(profile, bank, config, target_marks=20, seed=42)
    b = generate_manifest(profile, bank, config, target_marks=20, seed=42)

    assert a["question_ids"] == b["question_ids"]
    assert a["subject"] == "physics"
    assert a["score_band"] == "60-70"
    assert 0 < a["actual_marks"] <= 20
    assert len(a["question_ids"]) == len(set(a["question_ids"]))
    assert "Electricity and Magnetism" in a["chapter_marks"] or "Heat" in a["chapter_marks"]
