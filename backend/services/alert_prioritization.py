"""Deterministic alert prioritization helpers for Stage 2 kickoff scaffolding."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AlertPriorityInput:
    """Inputs required to calculate alert priority score."""

    alert_id: int
    severity: str
    risk_contribution: float
    distance_km: float
    sensitivity_match: int = 0
    fetched_at_epoch: int = 0


@dataclass(frozen=True)
class AlertPriorityResult:
    """Priority output payload used by future API response models."""

    alert_id: int
    priority_score: float
    urgency_label: str
    severity_score: float


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def _severity_score(severity: str) -> float:
    normalized = (severity or "").strip().lower()
    if normalized in {"extreme", "severe", "high"}:
        return 1.0
    if normalized in {"medium", "moderate"}:
        return 0.6
    return 0.3


def _distance_score(distance_km: float, max_radius_km: float = 250.0) -> float:
    safe_distance = max(0.0, distance_km)
    return 1.0 - min(safe_distance / max_radius_km, 1.0)


def _urgency_label(priority_score: float) -> str:
    if priority_score >= 75.0:
        return "high"
    if priority_score >= 45.0:
        return "medium"
    return "low"


def compute_priority(input_item: AlertPriorityInput) -> AlertPriorityResult:
    """Compute deterministic priority score with locked Stage 2 weights."""

    risk = _clamp(input_item.risk_contribution, 0.0, 1.0)
    distance = _distance_score(input_item.distance_km)
    severity = _severity_score(input_item.severity)
    sensitivity = _clamp(input_item.sensitivity_match / 5.0, 0.0, 1.0)

    priority = (0.45 * risk) + (0.25 * distance) + (0.20 * severity) + (0.10 * sensitivity)
    score = round(_clamp(priority, 0.0, 1.0) * 100.0, 2)

    return AlertPriorityResult(
        alert_id=input_item.alert_id,
        priority_score=score,
        urgency_label=_urgency_label(score),
        severity_score=severity,
    )


def sort_prioritized_alerts(inputs: list[AlertPriorityInput]) -> list[AlertPriorityResult]:
    """Sort alerts with deterministic tie-break logic from the Stage 2 policy lock."""

    computed = [compute_priority(item) for item in inputs]
    by_id = {item.alert_id: item for item in inputs}

    return sorted(
        computed,
        key=lambda item: (
            -item.priority_score,
            -item.severity_score,
            -by_id[item.alert_id].fetched_at_epoch,
            item.alert_id,
        ),
    )
