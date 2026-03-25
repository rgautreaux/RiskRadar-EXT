# RiskRadar Web Accessibility & Keyboard Navigation Guide

**Author:** Rebecca (Layout Lane)
**Last Updated:** 2026-03-23

## Purpose
This guide provides accessibility and keyboard navigation standards for all RiskRadar web pages, supporting QA/Docs and template work.

---

## Keyboard Navigation
- All interactive elements (links, buttons, form fields) must be reachable via Tab
- Use `:focus-visible` for clear focus outlines
- Navigation bar: left-to-right tab order, wraps to next row on mobile
- Modal/dialogs: trap focus within modal when open

---

## Accessibility Standards
- Use semantic HTML (header, nav, main, section, etc.)
- All icons/images must have descriptive `alt` text
- Sufficient color contrast (WCAG AA minimum)
- Use ARIA roles only when necessary (prefer native elements)
- Form fields must have associated `<label>`

---

## Testing Checklist
- [ ] Can all navigation and controls be used with keyboard only?
- [ ] Is focus visible and logical throughout?
- [ ] Are all icons/images accessible to screen readers?
- [ ] Is color contrast sufficient for text and UI elements?
- [ ] Are error/success states announced to assistive tech?

---

## Notes
- Update this guide as new accessibility needs arise
- QA/Docs Lane should reference this for parity checks
