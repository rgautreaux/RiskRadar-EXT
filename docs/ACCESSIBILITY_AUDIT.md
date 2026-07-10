# Accessibility Audit & Remediation Plan

**Project:** RiskRadar CMPS 357  
**Date:** May 8, 2026  
**Target:** WCAG 2.1 Level AA compliance

---

## 1. Automated Testing Setup

### Lighthouse CI
```bash
npm install -g @lhci/cli@^0.9.x
lhci autorun
```

### Axe-Core Playwright Integration
Already configured in `frontend/web/tests/e2e/accessibility.spec.js`

### Manual Checks
Use Chrome DevTools Accessibility Audit (Lighthouse tab in DevTools)

---

## 2. Common Issues & Fixes

### A. Color Contrast Issues

**Issue:** Text on background has insufficient contrast (< 4.5:1 for normal text, < 3:1 for large text)

**Check:**
```bash
# Use Chrome DevTools or WebAIM contrast checker
# https://webaim.org/resources/contrastchecker/
```

**Common fixes in `frontend/web/public/assets/app.css`:**

| Element | Current | Target | Fix |
|---------|---------|--------|-----|
| Body text on white | Black (#000) | Keep | ✅ Meets 21:1 |
| Links | Blue (#007BFF) | Darken to #0056B3 | Change color |
| Disabled buttons | Gray (#6C757D) | Darken to #5A6268 | Change color |
| Muted text | Gray (#6C757D) | Darken to #495057 | Change color |
| Focus outline | Default blue | Use contrasting color | Add custom outline |

### B. Missing Alt Text on Images

**Issue:** Images don't have descriptive `alt` attributes

**Check:** Use DevTools → Elements → search for `<img>` without `alt`

**Fix pattern:**
```php
// Before:
<img src="assets/icon-alert.svg">

// After:
<img src="assets/icon-alert.svg" alt="Alert notification icon">
```

### C. Form Labels Not Associated with Inputs

**Issue:** Input fields don't have `<label>` or `aria-label`

**Check:** DevTools → Accessibility pane → verify form field names

**Fix pattern:**
```php
// Before:
<input type="email" name="email" placeholder="Email">

// After:
<input type="email" name="email" id="email" aria-label="Email address">
<label for="email">Email address</label>
```

### D. Missing ARIA Labels on Buttons/Controls

**Issue:** Icon-only buttons lack accessible names

**Check:** Button should have visible text or `aria-label`

**Fix pattern:**
```php
// Before:
<button class="btn-close">×</button>

// After:
<button class="btn-close" aria-label="Close dialog">×</button>
```

### E. Heading Hierarchy Issues

**Issue:** Headings skip levels (H1 → H3) or multiple H1s

**Check:** DevTools → Accessibility → Inspect heading tree

**Fix:** Ensure sequential heading levels (H1 → H2 → H3, no skips)

### F. Keyboard Navigation Traps

**Issue:** Focus gets stuck in modals or can't reach controls

**Check:** 
1. Tab through entire page
2. Focus should move in logical order
3. Escape should close modals

**Fix:** Add `tabindex="0"` to focusable elements if needed; implement focus trap in modals

### G. No Focus Visible Styles

**Issue:** Focus outline is removed or invisible

**Check:** Tab through page; focus indicator should be visible

**Fix in CSS:**
```css
*:focus {
  outline: 2px solid #0066FF;
  outline-offset: 2px;
}
```

---

## 3. Files to Audit & Fix

### Frontend Files (Priority: High)

| File | Issue | Status |
|------|-------|--------|
| `frontend/web/public/assets/app.css` | Contrast, focus styles | Audit needed |
| `frontend/web/views/*.php` | Labels, alt text, ARIA | Audit needed |
| `frontend/web/public/assets/icons/*.svg` | Alt/title text | Audit needed |
| `frontend/web/components/layout.php` | Heading hierarchy | Audit needed |

### Backend Files (Priority: Medium)

| File | Issue | Status |
|------|-------|--------|
| `backend/api/*.py` | Error messages (logged, accessible) | OK |
| `backend/auth/security.py` | Rate limit UX (clear messages) | OK |

---

## 4. Accessibility Checklist

- [ ] **Contrast:** All text ≥ 4.5:1 (normal), ≥ 3:1 (large)
- [ ] **Images:** All non-decorative images have `alt` text
- [ ] **Forms:** All inputs have associated labels or `aria-label`
- [ ] **Buttons:** All buttons have accessible names (text or `aria-label`)
- [ ] **Headings:** Sequential levels (no skips), at least one H1 per page
- [ ] **Keyboard:** Full keyboard navigation; no traps; Escape closes modals
- [ ] **Focus:** Visible focus indicator on all focusable elements
- [ ] **Color:** Don't use color alone to convey info (use text, icons, patterns)
- [ ] **Motion:** No auto-playing animations > 5 seconds; respects `prefers-reduced-motion`
- [ ] **Language:** Page language declared in `<html lang="en">`
- [ ] **Responsive:** Content readable at 320px and 1920px
- [ ] **Screen Reader:** All landmarks, regions, and interactive elements announced

---

## 5. Quick Fixes (Low-Risk)

### Fix 1: Add Focus Styles to All Interactive Elements

**File:** `frontend/web/public/assets/app.css`

```css
/* Global focus style */
a:focus,
button:focus,
input:focus,
select:focus,
textarea:focus {
  outline: 3px solid #0066FF;
  outline-offset: 2px;
}

/* Remove default outline for mouse users (optional, more refined approach) */
:focus:not(:focus-visible) {
  outline: none;
}

:focus-visible {
  outline: 3px solid #0066FF;
  outline-offset: 2px;
}
```

### Fix 2: Improve Contrast on Muted Text

**File:** `frontend/web/public/assets/app.css`

```css
/* Muted/secondary text */
.text-muted,
.meta,
.subtitle {
  color: #495057;  /* Was #6C757D; now meets 4.5:1 on white */
}

/* Links */
a {
  color: #0056B3;  /* Was #007BFF; now meets 4.5:1 */
}
a:visited {
  color: #6610F2;
}
```

### Fix 3: Add ARIA Label to Close Button

**File:** `frontend/web/views/*.php` (search for close buttons)

```php
// Add aria-label to all close buttons:
<button class="close" aria-label="Close">×</button>
```

---

## 6. Testing Workflow

1. **Local testing (weekly):**
   ```bash
   npm run web:test:a11y
   ```

2. **Manual spot-checks (before commits):**
   - Tab through page; verify focus visible
   - Open in Edge with Narrator (Windows) or VoiceOver (macOS)
   - Check Lighthouse Accessibility score (target: ≥ 90)

3. **CI/CD gate (on PR):**
   - E2E accessibility tests in GitHub Actions
   - Axe violations fail the build if critical

---

## 7. Accessibility Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Screen Reader Testing](https://webaim.org/techniques/screenreader/)
- [MDN: Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [Lighthouse: Accessibility Scoring](https://developers.google.com/web/tools/lighthouse/v3/scoring#accessibility)

---

## 8. Next Steps

1. Run `npm run web:test:a11y` to identify critical violations
2. Apply fixes in priority order: contrast → labels → keyboard
3. Rerun tests and verify Lighthouse score ≥ 90
4. Document findings in this file
5. Commit fixes in focused PRs by violation type

**Estimated effort:** 2–4 hours for full audit + fixes  
**Target completion:** Before final submission
