# Stage 2 Implementation Specification (Kickoff Lock)

This document locks the initial Stage 2 implementation policy so development can begin without ambiguity.

## Scope Lock

- Stage 2 title: Environmental Risk Assessment and Alert Prioritization Extensions
- Required completion target: Week of 2026-04-28
- In scope for Stage 2:
  - Personal risk scoring engine
  - Smart alert prioritization
  - API exposure for score and prioritized alerts
  - Web and mobile baseline UI integration
- Out of scope for Stage 2:
  - Stage 3 map implementation
  - Stage 4 forecasting/assistant implementation

## Scoring Model Lock (S2-01)

### Score Output

- Primary score range: 0-100
- Tier labels:
  - Low: 0-39
  - Medium: 40-69
  - High: 70-100

### Risk Inputs

All component inputs are normalized to 0.0-1.0:

- Air quality risk
- Weather risk
- Wildfire risk
- Pollution risk

### Base Weighted Formula

Base score before sensitivity multiplier:

- base = (0.35 * air_quality)
  + (0.20 * weather)
  + (0.25 * wildfire)
  + (0.20 * pollution)

### Sensitivity Model

- Sensitivity fields use 0-5 scale per factor.
- Average sensitivity = mean of configured factor sensitivities.
- Sensitivity multiplier:
  - multiplier = 1.0 + (avg_sensitivity * 0.08)
- Final score:
  - final = clamp(base * multiplier, 0.0, 1.0) * 100

### Missing-Data Defaults

- Missing sensitivity factors default to 0.
- Missing normalized risk factors default to 0.0.
- Missing user location does not fail score computation; distance-based terms are handled in prioritization fallback logic.

## Prioritization Policy Lock (S2-05)

### Priority Score Inputs

- risk_contribution (normalized from personal risk impact)
- distance_score (from user-to-alert distance)
- severity_score
- sensitivity_match_score

### Normalization Rules

- risk_contribution: normalized 0.0-1.0
- distance_score:
  - max relevance radius: 250 km
  - distance_score = 1.0 - min(distance_km / 250.0, 1.0)
- severity_score map:
  - extreme/severe/high: 1.0
  - medium/moderate: 0.6
  - low/other: 0.3
- sensitivity_match_score:
  - sensitivity_value / 5.0

### Weighted Priority Formula

- priority = (0.45 * risk_contribution)
  + (0.25 * distance_score)
  + (0.20 * severity_score)
  + (0.10 * sensitivity_match_score)

- priority_score = round(priority * 100, 2)

### Urgency Labels

- High: >= 75
- Medium: >= 45 and < 75
- Low: < 45

### Deterministic Tie-Break Order (S2-06)

When two alerts have equal priority_score:

1. Higher severity_score first
2. More recent fetched_at first
3. Smaller alert id first

## API Contract Strategy Lock (S2-04 / S2-07)

- Preserve existing Stage 1 alerts contract at GET /api/v1/alerts.
- Add new prioritized route:
  - GET /api/v1/alerts/prioritized
- Add user risk score route:
  - GET /api/v1/users/{user_id}/risk-score

## Implementation Scaffolding Targets

- Backend service modules:
  - backend/services/risk_scoring.py
  - backend/services/alert_prioritization.py
- Mobile prep modules:
  - frontend/mobile/RiskRadar/services/riskService.ts
  - frontend/mobile/RiskRadar/hooks/useRiskData.ts
- Web prep integration:
  - frontend/web/public/risk.php
  - frontend/web/views/risk.php
  - frontend/web/services/api_client.php

## Verification Gates Before Stage 2 Completion

- Determinism: identical inputs produce identical score and priority ordering.
- Contract stability: Stage 1 route responses remain unchanged.
- Fallback behavior: missing data handled without crashes.
- Cross-client parity: web and mobile display backend-prioritized ordering.

## Ownership Start Map

- Max: S2-01, S2-03, S2-04, S2-05, S2-06, S2-07, S2-09
- Rebecca: S2-02, S2-08, DOC synchronization
- Shared review checkpoints: weekly sync and acceptance gate reviews
