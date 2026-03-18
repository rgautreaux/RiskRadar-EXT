from backend.services.alert_prioritization import (
    AlertPriorityInput,
    compute_priority,
    sort_prioritized_alerts,
)
from backend.services.risk_scoring import RiskFactors, UserSensitivities, compute_risk_score


def test_risk_score_scaffolding_is_deterministic():
    factors = RiskFactors(air_quality=0.7, weather=0.4, wildfire=0.2, pollution=0.6)
    sensitivities = UserSensitivities(air_quality=3, weather=1, wildfire=2, pollution=4)

    first = compute_risk_score(factors, sensitivities)
    second = compute_risk_score(factors, sensitivities)

    assert first == second
    assert 0.0 <= first.score <= 100.0


def test_priority_scaffolding_sorts_with_tiebreaks():
    inputs = [
        AlertPriorityInput(alert_id=2, severity='high', risk_contribution=0.6, distance_km=20, sensitivity_match=3, fetched_at_epoch=100),
        AlertPriorityInput(alert_id=1, severity='high', risk_contribution=0.6, distance_km=20, sensitivity_match=3, fetched_at_epoch=200),
    ]

    ordered = sort_prioritized_alerts(inputs)

    assert len(ordered) == 2
    assert ordered[0].alert_id == 1
    assert ordered[1].alert_id == 2


def test_priority_scaffolding_uses_labeled_output():
    result = compute_priority(
        AlertPriorityInput(
            alert_id=99,
            severity='severe',
            risk_contribution=1.0,
            distance_km=0.0,
            sensitivity_match=5,
            fetched_at_epoch=500,
        )
    )

    assert result.urgency_label in {'high', 'medium', 'low'}
