# Accessibility Checklist: RiskRadar UI (Stage 4+)

## General
- [x] All interactive elements are reachable and usable via keyboard (Tab/Shift+Tab, Enter, Space).
- [x] All headings use semantic HTML (`<h1>`, `<h2>`, etc.) and follow a logical order.
- [x] All lists use `<ul>`, `<ol>`, or `<dl>` as appropriate.
- [x] All details/expandable sections use `<details>` and `<summary>`.
- [x] All images/icons have descriptive `alt` text.
- [x] All color contrast ratios meet WCAG AA standards (4.5:1 for normal text).
- [x] Visually hidden text is used for screen readers where needed.
- [x] ARIA labels/roles are used for complex regions (e.g., `role="region"`, `aria-label`).

## Risk Score Breakdown Section
- [x] Section has an accessible heading (`<h2 id="risk-score-heading">`).
- [x] Section is labeled as a region for screen readers (`role="region"`, `aria-labelledby`).
- [x] Risk score and level are announced with `aria-live` for dynamic updates.
- [x] Factor list uses `<ul>` and `<li>` for clarity.
- [x] Formula explanation uses `<details>` and `<summary>` for expand/collapse.
- [x] All text and backgrounds have sufficient contrast.
- [x] Section is navigable and usable with keyboard only.

## Personalization & Feedback
- [x] Profile page is accessible and allows updating preferences with keyboard/screen reader.
- [x] Smart alerts and alert detail pages reflect personalization changes.
- [x] Guest users see appropriate messaging and locked features are clearly indicated.

## Testing
- [x] Manual keyboard navigation test.
- [x] Screen reader test (NVDA, VoiceOver, or similar).
- [x] Color contrast test (using browser dev tools or online checker).

---

All items should be checked before release. Document any exceptions or limitations found during testing.