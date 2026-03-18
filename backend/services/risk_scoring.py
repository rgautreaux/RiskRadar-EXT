"""Deterministic risk scoring helpers for Stage 2 kickoff scaffolding."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskFactors:
    """Normalized environmental factors in the 0.0-1.0 range."""

    air_quality: float = 0.0
    weather: float = 0.0
    wildfire: float = 0.0
    pollution: float = 0.0


@dataclass(frozen=True)
class UserSensitivities:
    """Per-factor sensitivity values in the 0-5 range."""

    air_quality: int = 0
    weather: int = 0
    wildfire: int = 0
    pollution: int = 0


@dataclass(frozen=True)
class RiskScoreResult:
    """Output shape used by future API schema mapping."""

    score: float
    level: str
    base_score: float
    multiplier: float


FACTOR_WEIGHTS = {
    "air_quality": 0.35,
    "weather": 0.20,
    "wildfire": 0.25,
    "pollution": 0.20,
}


def _clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def _risk_level(score: float) -> str:
    if score >= 70.0:
        return "high"
    if score >= 40.0:
        return "medium"
    return "low"


def _sensitivity_multiplier(sensitivities: UserSensitivities) -> float:
    values = [
        sensitivities.air_quality,
        sensitivities.weather,
        sensitivities.wildfire,
        sensitivities.pollution,
    ]
    avg = sum(_clamp(float(v), 0.0, 5.0) for v in values) / len(values)
    return 1.0 + (avg * 0.08)


def compute_risk_score(
    factors: RiskFactors,
    sensitivities: UserSensitivities,
) -> RiskScoreResult:
    """Compute a deterministic 0-100 risk score using the Stage 2 locked policy."""

    base = (
        FACTOR_WEIGHTS["air_quality"] * _clamp(factors.air_quality, 0.0, 1.0)
        + FACTOR_WEIGHTS["weather"] * _clamp(factors.weather, 0.0, 1.0)
        + FACTOR_WEIGHTS["wildfire"] * _clamp(factors.wildfire, 0.0, 1.0)
        + FACTOR_WEIGHTS["pollution"] * _clamp(factors.pollution, 0.0, 1.0)
    )

    multiplier = _sensitivity_multiplier(sensitivities)
    final = _clamp(base * multiplier, 0.0, 1.0) * 100.0
    score = round(final, 2)

    return RiskScoreResult(
        score=score,
        level=_risk_level(score),
        base_score=round(base * 100.0, 2),
        multiplier=round(multiplier, 3),
    )
