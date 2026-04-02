# Accessibility & Navigation Test Script — Stage 3 Web Map

## 1. Keyboard Navigation
- [ ] Tab/Shift+Tab cycles through all overlay toggles, region filter, user ID input, and map container.
- [ ] Tab/Shift+Tab cycles through alert markers on the map (when map is focused).
- [ ] Enter/Space toggles overlays and opens marker details modal when focused.
- [ ] Alt+1–7 keyboard shortcuts toggle overlays.
- [ ] Arrow keys pan the map, +/- zooms when map is focused.

## 2. Screen Reader & ARIA
- [ ] All controls have appropriate aria-label, aria-checked, aria-describedby, and role attributes.
- [ ] Overlay group has role="group" and aria-label.
- [ ] Map container has role="region" and aria-live="polite".
- [ ] Overlay toggling and marker focus are announced (toast or live region).

## 3. Modal Accessibility
- [ ] Marker details modal has role="dialog", aria-modal, and aria-labelledby.
- [ ] Modal traps focus and closes with Escape.
- [ ] Modal is reachable by keyboard and screen reader.

## 4. Responsive & Visual
- [ ] All controls and map are usable on mobile and desktop.
- [ ] Overlay colors meet WCAG contrast guidelines.

## 5. Automated Accessibility
- [ ] Run axe-core or Lighthouse in browser DevTools; confirm no critical accessibility violations.

---
If any test fails, note the issue and update code or docs as needed.
