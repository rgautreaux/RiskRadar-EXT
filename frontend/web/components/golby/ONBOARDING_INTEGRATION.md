# Golby Onboarding & Assistant Integration

## Overview
This document describes the implementation and integration of the Golby onboarding tutorial and assistant widget in the RiskRadar web application (Stage 4).

## Key Features
- **Onboarding Tutorial:**
  - Golby leads new users through a step-by-step tutorial on first login.
  - Tutorial covers navigation, dashboard, alerts, summaries, risk scoring, and assistant features.
  - Completion is tracked in the backend (`has_completed_onboarding` field in user model).
- **Assistant Widget:**
  - Golby is available as a persistent chat/help widget on all main pages.
  - Context-aware, with responses tailored to user profile and current page.
  - Guardrails for safety and appropriate advice.
- **Accessibility:**
  - All Golby visuals have alt text and ARIA labels.
  - Keyboard navigation and high-contrast support.

## Backend Integration
- User model includes `has_completed_onboarding` (boolean).
- API endpoint: `PATCH /api/v1/users/{user_id}/complete_onboarding` to mark onboarding as complete.
- Onboarding state is returned in user API responses.

## Frontend Integration
- `GolbyAssistantWidget.tsx` manages onboarding logic and chat UI.
- `apiClient.ts` provides API calls for onboarding completion.
- `OnboardingTutorial.tsx` defines tutorial steps and UI.
- Golby icon assets are in `UI_UX_STYLE_FILES/assets/Golby_Expression_Draft/`.

## Usage
- New users are automatically shown the onboarding tutorial.
- Returning users can access Golby for help at any time.
- Tutorial can be customized by editing `OnboardingTutorial.tsx`.

## Testing & Verification
- See `USER_GUIDE.md` for end-to-end usage instructions.
- See `DEMO_ONBOARDING.md` for demo and test scenarios.
- Run backend and frontend, register a new user, and verify onboarding flow.

## Accessibility
- Test with keyboard and screen reader for full compliance.
- All interactive elements are reachable and labeled.

## References
- [USER_GUIDE.md](../../USER_GUIDE.md)
- [DEMO_ONBOARDING.md](../../docs/DEMO_ONBOARDING.md)
- [GOLBY_ICON_PLAN.md](../../docs/PLANNING_DOCS/STAGE4_DOCS/GOLBY_ICON_PLAN.md)
