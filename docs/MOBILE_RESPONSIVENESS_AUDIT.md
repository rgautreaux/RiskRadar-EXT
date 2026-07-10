# Mobile Responsiveness Audit & Fixes (360px-768px)

**Project:** RiskRadar CMPS 357  
**Scope:** Frontend responsiveness on mobile devices  
**Target:** Fully functional at 360px, 480px, 768px viewports

---

## 1. Pages to Test (Priority Order)

| Page | Route | Issues | Status |
|------|-------|--------|--------|
| Login | `/login.php` | Button sizing, form width | Test |
| Register | `/register.php` | Form labels, input width | Test |
| Dashboard | `/index.php` | Stat grid, alert list | Test |
| Alerts | `/alerts.php` | Filter bar, card layout | Test |
| Summaries | `/summaries.php` | Summary cards, text overflow | Test |
| Map | `/map.php` | Legend position, marker tap | Test |
| Forecast | `/forecast.php` | Chart height, timeline scroll | Test |
| Assistant | `/assistant.php` | Widget size, chat input | Test |
| Profile | `/profile.php` | Form fields, checkbox grid | Test |

---

## 2. Known Mobile Issues & Fixes

### Issue: Form inputs too small or cramped on mobile

**Symptoms:** Text input fields hard to tap (< 44px height), labels cut off

**Fix:**
```css
@media (max-width: 480px) {
  input, select, textarea {
    min-height: 44px;  /* Touch-friendly minimum */
    font-size: 16px;   /* Prevents zoom on iOS */
    padding: 12px;
  }
  
  label {
    display: block;
    margin-bottom: 8px;
  }
}
```

### Issue: Stat strip breaks into too many rows

**Symptoms:** Stats grid columns too narrow, text wraps awkwardly

**Fix:**
```css
@media (max-width: 640px) {
  .dash-stat-strip {
    grid-template-columns: repeat(2, 1fr);
  }
  
  @media (max-width: 480px) {
    .dash-stat-strip {
      grid-template-columns: 1fr;
    }
  }
}
```

### Issue: Map legend overlaps map content on mobile

**Symptoms:** Legend hides markers, not scrollable

**Fix:**
```css
@media (max-width: 768px) {
  #risk-map-legend {
    max-height: 30vh;
    overflow-y: auto;
    position: relative;
    z-index: 5;
  }
}
```

### Issue: Assistant widget too large, chat input hard to tap

**Symptoms:** Widget > 100vw, chat input button missing or off-screen

**Fix:**
```css
@media (max-width: 480px) {
  #riskradar-ai-assistant-widget {
    width: 100vw !important;
    max-width: 100vw;
    bottom: 0 !important;
    right: 0 !important;
    border-radius: 0;
    max-height: 80vh;
  }
  
  .chat-input-button {
    min-height: 44px;
    min-width: 44px;
  }
}
```

### Issue: Filter bar buttons wrap awkwardly, become hard to use

**Symptoms:** Buttons stack vertically, unclear which filter applies to which input

**Fix:**
```css
@media (max-width: 640px) {
  .filter-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .filter-grid button {
    width: 100%;
  }
}
```

### Issue: Alert/summary cards too narrow, text hard to read

**Symptoms:** Card padding crushes text, hard to read on 360px

**Fix:**
```css
@media (max-width: 480px) {
  .alert-card, .summary-card {
    padding: 12px;  /* Reduce padding */
    margin-bottom: 12px;
  }
  
  .alert-card h2, .summary-card h2 {
    font-size: 1rem;  /* Slightly smaller */
  }
  
  .severity-pill, .meta-chip {
    display: block;  /* Stack instead of inline */
    margin-bottom: 4px;
  }
}
```

### Issue: Navigation links too small or not touch-friendly

**Symptoms:** Links easy to tap on desktop (16px padding) but feel cramped on mobile

**Fix:**
```css
@media (max-width: 768px) {
  .topnav a {
    padding: 12px;
    min-height: 44px;
    display: flex;
    align-items: center;
  }
}
```

---

## 3. Testing Workflow

### A. Manual Mobile Testing

1. **Use Chrome DevTools:**
   ```
   1. Open DevTools (F12)
   2. Click device icon (mobile emulation)
   3. Select "iPhone 12" or "Pixel 5" presets
   4. Test at 360px, 480px, 768px
   ```

2. **Test each page:**
   - Can you read all text without horizontal scroll?
   - Can you tap all buttons/links (> 44px)?
   - Does the layout look intentional (not broken)?
   - Do form inputs accept text?

3. **Document issues:**
   - Take screenshots at 360px showing the problem
   - Note: Button size, text overflow, layout breaks

### B. Automated Testing (via Playwright)

```bash
npm run web:test:e2e
```

The `mobile-responsive.spec.js` suite already checks:
- Guest flow on 360px
- Alerts page responsive layout
- Map page responsive controls

### C. Real Device Testing (Optional)

If available, test on actual mobile phone:
- iOS 14+ (Safari)
- Android 11+ (Chrome)
- Test touchscreen interactions (tap buttons, scroll, pinch-zoom on map)

---

## 4. Responsive Breakpoints in Project

Current breakpoints in `app.css`:

```css
@media (max-width: 700px) { /* Tablet */
@media (max-width: 480px) { /* Mobile */
@media (max-width: 640px) { /* Mobile-to-tablet transition */
```

Add if missing:
- `@media (max-width: 360px)` — Extra-small phones (iPhone SE, older Android)
- `@media (max-width: 768px)` — Tablet (iPad mini)

---

## 5. Checklist for Mobile Fixes

- [ ] All inputs and buttons ≥ 44px height on mobile
- [ ] No horizontal scrolling at 360px (content fits within viewport)
- [ ] Text readable without zooming (16px+ font size on inputs)
- [ ] Form labels visible and associated with inputs
- [ ] Stat grids stack intelligently (1–2 columns on mobile)
- [ ] Map legend doesn't cover markers; scrollable if > 30% height
- [ ] Assistant widget doesn't exceed viewport width
- [ ] Navigation links touch-friendly (12–16px padding)
- [ ] Filter buttons stack/arrange sensibly on mobile
- [ ] Alert/summary cards readable at 360px (adequate padding, not crushed)
- [ ] No visual regressions at 768px (tablet size)

---

## 6. Screenshot Evidence Locations

After fixes, save mobile screenshots:
```
static/evidence/
├── mobile_360_dashboard.png
├── mobile_360_alerts.png
├── mobile_360_map.png
├── mobile_360_assistant.png
└── ...
```

Use in PRs and final submission to show mobile UX works.

---

## 7. Potential Regression Areas

**High Risk (test after changes):**
- Dashboard stat grid layout
- Map marker popup positioning on mobile
- Assistant widget sizing
- Form input styling (especially on iOS with automatic zoom)

**Medium Risk:**
- Navigation/topnav wrapping behavior
- Card padding and text overflow
- Filter bar arrangement

---

## Next Steps

1. Run E2E tests on 360px viewport (`npm run web:test:e2e`)
2. Manually test each page at 360px, 480px, 768px using DevTools
3. Document issues with screenshots
4. Apply fixes from Section 2 above
5. Retest and verify responsive breakpoints work
6. Commit fixes in a focused PR with "mobile: " prefix
7. Add evidence screenshots to `static/evidence/`

**Estimated effort:** 1–2 hours for testing + applying low-risk CSS fixes
