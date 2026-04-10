"""Soft-learning personality helpers for Golby assistant responses."""

from __future__ import annotations

import json
from copy import deepcopy
from datetime import datetime, timezone


DEFAULT_PROFILE = {
    "tone": {
        "warmth": 0.55,
        "calmness": 0.75,
        "humor": 0.40,
    },
    "delivery": {
        "conciseness": 0.70,
        "detail": 0.45,
        "expandability": 0.55,
    },
    "voice": {
        "formality": 0.35,
    },
    "learning": {
        "feedback_count": 0,
        "last_feedback_at": None,
    },
}


def _clamp(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    return max(min_value, min(max_value, round(value, 4)))


def default_profile_json() -> str:
    return json.dumps(DEFAULT_PROFILE)


def parse_profile(raw_profile: str | None) -> dict:
    if not raw_profile:
        return deepcopy(DEFAULT_PROFILE)

    try:
        loaded = json.loads(raw_profile)
    except json.JSONDecodeError:
        return deepcopy(DEFAULT_PROFILE)

    profile = deepcopy(DEFAULT_PROFILE)
    for section in ("tone", "delivery", "voice", "learning"):
        if isinstance(loaded.get(section), dict):
            profile[section].update(loaded[section])

    return profile


def serialize_profile(profile: dict) -> str:
    return json.dumps(profile)


def _contains_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def apply_feedback_to_profile(
    profile: dict,
    reaction: str,
    rating: int,
    comment: str | None = None,
) -> dict:
    updated = deepcopy(profile)
    tone = updated["tone"]
    delivery = updated["delivery"]
    voice = updated["voice"]
    learning = updated["learning"]

    reaction_key = (reaction or "").lower().strip()
    if reaction_key in {"thumbs_up", "smile"}:
        tone["warmth"] = _clamp(tone["warmth"] + 0.04)
        tone["calmness"] = _clamp(tone["calmness"] + 0.02)
        if reaction_key == "smile":
            tone["humor"] = _clamp(tone["humor"] + 0.05)
    elif reaction_key == "thumbs_down":
        tone["humor"] = _clamp(tone["humor"] - 0.06)
        delivery["conciseness"] = _clamp(delivery["conciseness"] + 0.03)

    if rating >= 4:
        tone["warmth"] = _clamp(tone["warmth"] + 0.02)
        tone["calmness"] = _clamp(tone["calmness"] + 0.02)
    elif rating <= 2:
        delivery["conciseness"] = _clamp(delivery["conciseness"] + 0.04)
        delivery["detail"] = _clamp(delivery["detail"] - 0.03)

    lower_comment = (comment or "").lower()
    if lower_comment:
        if _contains_any(lower_comment, ("too long", "verbose", "wordy", "ramble")):
            delivery["conciseness"] = _clamp(delivery["conciseness"] + 0.08)
            delivery["detail"] = _clamp(delivery["detail"] - 0.07)
        if _contains_any(lower_comment, ("too short", "expand", "more detail", "explain more")):
            delivery["detail"] = _clamp(delivery["detail"] + 0.08)
            delivery["conciseness"] = _clamp(delivery["conciseness"] - 0.05)
        if _contains_any(lower_comment, ("robotic", "stiff", "cold", "formal")):
            tone["warmth"] = _clamp(tone["warmth"] + 0.06)
            voice["formality"] = _clamp(voice["formality"] - 0.06)
        if _contains_any(lower_comment, ("wrong", "incorrect", "inaccurate")):
            tone["humor"] = _clamp(tone["humor"] - 0.07)
            tone["calmness"] = _clamp(tone["calmness"] + 0.03)

    learning["feedback_count"] = int(learning.get("feedback_count", 0)) + 1
    learning["last_feedback_at"] = datetime.now(timezone.utc).isoformat()
    return updated


def _wants_expansion(message: str) -> bool:
    lower = (message or "").lower()
    return any(
        phrase in lower
        for phrase in (
            "expand",
            "more detail",
            "explain more",
            "full breakdown",
            "why",
            "walk me through",
        )
    )


def shape_reply(reply: str, category: str, profile: dict, message: str) -> str:
    if category == "guardrail":
        return reply

    tone = profile["tone"]
    delivery = profile["delivery"]

    shaped = reply.strip()
    wants_expansion = _wants_expansion(message)

    if delivery["conciseness"] >= 0.78 and not wants_expansion and len(shaped) > 220:
        first_sentence = shaped.split(". ")[0].strip()
        if first_sentence and not first_sentence.endswith("."):
            first_sentence += "."
        shaped = first_sentence or shaped

    if tone["warmth"] >= 0.68 and not shaped.lower().startswith("i cannot"):
        shaped = "Absolutely. " + shaped

    if tone["humor"] >= 0.72 and category != "guardrail":
        shaped += " We can keep this steady and low-stress, Golby-style."

    if wants_expansion:
        shaped += " I can also provide a step-by-step breakdown if you want even deeper detail."
    elif delivery["expandability"] >= 0.50:
        shaped += " I can expand on this if you want more detail."

    return shaped
