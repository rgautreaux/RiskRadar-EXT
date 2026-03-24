# RiskRadar Web Design Tokens & Spacing Guide

**Author:** Rebecca (Layout Lane)
**Last Updated:** 2026-03-23

## Purpose
This guide documents the global spacing rhythm, breakpoints, and design tokens for consistent UI/UX across all RiskRadar web pages.

---

## Spacing Rhythm
- `--space-xs`: 4px (micro spacing)
- `--space-sm`: 8px (tight spacing)
- `--space-md`: 24px (default section gap)
- `--space-lg`: 40px (major region gap)
- `--space-xl`: 64px (hero/outer margin)

**Usage:**
- Use these tokens for all margin and padding in CSS.
- Prefer `.gap-md` or `.gap-lg` for grid/flex layouts.

---

## Breakpoints
- **Desktop:** 900px and up
- **Tablet:** 600px – 899px
- **Mobile:** below 600px

**Responsive rules:**
- Reduce padding/gap at each breakpoint (see app.css for details)
- Navigation and topbar stack vertically on mobile

---

## CSS Variable Mapping
- All theme colors and spacing values are defined as CSS variables in theme_tokens.css and referenced in app.css.
- Hardcoded values in CSS/HTML are being refactored to use these variables for consistency.
- For new tokens, propose additions here before using in templates.

## Design Tool Mapping
- Figma/XD/Sketch inspect tool values for spacing, font sizes, and colors are cross-checked against these CSS variables.
- Any mismatches are documented and flagged for correction or rationale.

## UI Pattern Documentation
- Standard UI patterns (buttons, cards, spacing, typography, icon usage) are listed here and in WIREFRAME_STYLE_IMPLEMENTATION.md.
- Deviations from the wireframe are documented with annotated screenshots, rationale, date, and author.

---

## Design Tokens
- Colors: see `:root` in app.css for all color variables
- Typography: use `.text-xs`, `.text-sm`, `.text-md`, `.text-lg`, `.text-xl`
- Icon slots: use `.icon-slot`, `.icon-badge` for consistent icon backgrounds

---

## Example
```css
.section {
  padding: var(--space-lg) 0;
  gap: var(--space-md);
}
```

---

## Notes
- Only update this guide and app.css for global changes.
- For new spacing or token needs, propose additions here before using in templates.
