# Golby Assistant Widget & Onboarding Tutorial

## Overview
Golby is the RiskRadar AI assistant and onboarding guide, designed to help new users learn the app and provide contextual help throughout the user experience. Golby appears as a mascot icon and interactive chat widget, and leads new users through a step-by-step onboarding tutorial on their first login.

## Features
- **Onboarding Tutorial:**
  - Automatically triggers for new users (those who have not completed onboarding).
  - Walks users through key features of the app with popups and contextual tips.
  - Tracks completion in the backend (`has_completed_onboarding` flag).
- **Assistant Widget:**
  - Persistent chat/help widget available on all main pages.
  - Context-aware, with responses tailored to user profile and current page.
  - Guardrails for safety and appropriate advice.
- **Accessibility:**
  - All Golby visuals have alt text and ARIA labels.
  - Keyboard navigation and high-contrast support.

## Integration
- **Backend:**
  - Onboarding state is tracked in the user model and exposed via API.
  - API endpoint: `PATCH /api/v1/users/{user_id}/complete_onboarding`
- **Frontend:**
  - `GolbyAssistantWidget.tsx` manages onboarding logic and chat UI.
  - `apiClient.ts` provides API calls for onboarding completion.
  - Tutorial steps and UI are defined in `OnboardingTutorial.tsx`.

## Usage
- Golby icon appears in the lower-right corner of the app.
- New users are greeted with the onboarding tutorial.
- Returning users can access Golby for help at any time.

## Customization
- Tutorial steps can be edited in `OnboardingTutorial.tsx`.
- Golby icon assets are in `UI_UX_STYLE_FILES/assets/Golby_Expression_Draft/`.
- To change onboarding logic, update the backend user model and API as needed.

## Developer Notes
- Ensure backend and frontend are both running for full onboarding flow.
- See `USER_GUIDE.md` and `DEMO_ONBOARDING.md` for end-to-end demo instructions.
- For accessibility, test with keyboard and screen reader.
