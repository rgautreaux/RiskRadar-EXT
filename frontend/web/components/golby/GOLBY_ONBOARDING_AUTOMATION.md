# Golby Onboarding & Assistant: Automated Test Coverage Summary

This document summarizes the automated test coverage for the Golby onboarding and assistant features.

---

## Automated Test Scripts

### 1. `test_golby_onboarding.js`
- Verifies onboarding tutorial appears for new users
- Confirms onboarding does not repeat for returning users

### 2. `test_golby_onboarding_extended.js`
- Registers a new user and completes onboarding
- Simulates tutorial step completion (clicks next/finish)
- Verifies onboarding does not repeat after completion
- Opens assistant widget and tests:
  - Contextual response to normal queries
  - Guardrail response to dangerous queries
- Verifies keyboard navigation and accessibility:
  - Tabs to Golby icon
  - Opens widget and tabs to input/send button

---

## How to Run

1. Start backend and frontend servers.
2. In project root, run:
   ```
   npx jest frontend/web/tests/test_golby_onboarding.js
   npx jest frontend/web/tests/test_golby_onboarding_extended.js
   ```

---

## Coverage Notes
- Covers first-time user onboarding, repeat login, assistant chat, guardrails, and accessibility.
- Backend API state check is included as a comment (add fetch if API allows public user state query).
- Extend with more flows as needed (e.g., API token auth, admin scenarios).

---

For manual and demo walkthroughs, see `GOLBY_ONBOARDING_DEMO.md` and `GOLBY_ONBOARDING_CHECKLIST.md`.
