# ARIA and Live Region Guidelines for RiskRadar Web

**Author:** Rebecca (Layout Lane)
**Last Updated:** 2026-03-23

## Purpose
This guide provides ARIA labeling and live region usage standards for dynamic content (alerts, modals, etc.)

---

## ARIA Labeling
- Use `aria-label` or `aria-labelledby` for all custom controls
- Use `aria-describedby` for additional context (e.g., error messages)
- Use `role="button"`, `role="dialog"`, etc., only when native elements are not possible

## Live Regions
- Use `aria-live="polite"` for non-critical updates (e.g., status messages)
- Use `aria-live="assertive"` for urgent alerts (e.g., error popups)
- Use `aria-atomic="true"` to ensure full message is read

## Example
```html
<div role="alert" aria-live="assertive" aria-atomic="true">Error: Unable to save changes.</div>
```

## Notes
- Only use ARIA roles/attributes when native HTML is insufficient
- Test with screen readers to verify announcements
