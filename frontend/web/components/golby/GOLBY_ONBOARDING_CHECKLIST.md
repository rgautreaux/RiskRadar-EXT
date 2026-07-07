# Golby Onboarding & Assistant: Scenario Verification Checklist

This checklist covers all scenarios for the Golby onboarding and assistant features. Use this to verify implementation and demo readiness.

---

## 1. Onboarding Tutorial (First-Time User)
- [ ] Register a new user
- [ ] Log in as new user
- [ ] Onboarding tutorial appears automatically
- [ ] Complete tutorial steps
- [ ] Backend `has_completed_onboarding` is set to `true`
- [ ] Log out and log in again: onboarding does not repeat

## 2. Assistant Widget (General Use)
- [ ] Golby icon visible on all main pages
- [ ] Widget opens on click
- [ ] Chat accepts input and returns contextual responses
- [ ] Guardrails activate for inappropriate queries

## 3. Accessibility
- [ ] All onboarding/tutorial steps are keyboard navigable
- [ ] All assistant/chat UI is keyboard navigable
- [ ] Screen reader announces all popups, buttons, and chat messages
- [ ] Alt text and ARIA labels present

## 4. API & Backend
- [ ] API returns correct onboarding state for user
- [ ] PATCH endpoint updates onboarding state

## 5. Automated Test
- [ ] Run `test_golby_onboarding.js` and confirm all tests pass

## 6. Demo Walkthrough
- [ ] Register new user, show onboarding
- [ ] Complete onboarding, log out/in, show onboarding does not repeat
- [ ] Open assistant, ask questions, show guardrails
- [ ] Demonstrate accessibility
- [ ] Show API onboarding state

---

For details, see: `GOLBY_ONBOARDING_DEMO.md`, `ONBOARDING_INTEGRATION.md`, `USER_GUIDE.md`.
