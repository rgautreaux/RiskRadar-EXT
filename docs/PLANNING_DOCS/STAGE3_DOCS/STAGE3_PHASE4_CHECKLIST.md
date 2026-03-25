# Stage 3 Phase 4: Manual Verification Checklist

This checklist is designed to ensure all Stage 3 web-app features (excluding mobile) are fully implemented, accessible, and ready for grading. Use this as a guide for manual testing and evidence collection.

## 1. Map Overlays & Interactivity
- [ ] Map loads successfully with default overlays
- [ ] Overlay toggles (e.g., risk, alerts, air quality) work as expected
- [ ] Multiple overlays can be enabled/disabled independently
- [ ] Overlay legend updates to reflect active overlays
- [ ] Map responds to pan/zoom and overlays update accordingly

## 2. Personalized Risk Overlay
- [ ] User ID input is visible and accessible (label, ARIA, focus)
- [ ] Entering a valid user ID fetches personalized overlay
- [ ] Personalized overlay is visually distinct (legend, color, tooltip)
- [ ] Switching user IDs updates overlay as expected
- [ ] Invalid/missing user ID shows error or fallback state

## 3. Accessibility
- [ ] All controls (toggles, user ID input) are keyboard accessible
- [ ] ARIA labels and descriptions are present and correct
- [ ] Sufficient color contrast for overlays and UI elements
- [ ] Focus indicators are visible for all interactive elements
- [ ] Map and overlays are screen reader friendly (test with NVDA/VoiceOver)

## 4. Error Handling & Fallbacks
- [ ] Network/API errors show user-friendly messages
- [ ] Overlay fetch failures do not break map UI
- [ ] Legend/tooltips update to reflect error/fallback states

## 5. Documentation & Guidance
- [ ] User Guide documents all map features and workflows
- [ ] Legend/tooltips explain overlays and personalized mode
- [ ] Accessibility features are described in documentation

## 6. Evidence Collection
- [ ] Annotated screenshots of map with overlays (default, personalized, error states)
- [ ] Screen recording of map interactivity and accessibility features
- [ ] Evidence files are organized for grading (e.g., in /static or /docs)

---

**Instructions:**
- Check each item as you verify it.
- Capture screenshots/recordings as you go.
- Note any issues or deviations for follow-up.
- Ensure all evidence is saved and referenced in documentation.
