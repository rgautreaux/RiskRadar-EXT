Stage 3 (S3-06) Manual Evidence Capture — Checklist for Max
============================================================

**Objective:** Capture desktop, mobile, and video evidence for the RiskRadar interactive map (Stage 3, Deliverable 3).

**Timeline:** Before final submission  
**Assigned to:** Max  
**Status:** Ready to execute (grading team can proceed after captures)

---

## Prerequisites

1. **Backend running:**
   ```bash
   cd backend
   .venv\Scripts\activate  # or source .venv/bin/activate on macOS/Linux
   uvicorn main:app --host 127.0.0.1 --port 8001
   ```

2. **Frontend running (PHP):**
   ```bash
   # From project root
   php -S 127.0.0.1:8080 -t frontend/web/public
   ```

3. **Demo data seeded:**
   ```bash
   npm run demo:setup
   ```

4. **Environment set:** Login as guest, and later as authenticated user (register a test account).

---

## Capture Sequence

### Part 1: Desktop Screenshots (1280px viewport)

**1.1 Map Overview — All Layers & Legend**
- Navigate to `http://127.0.0.1:8080/map.php` as guest
- Ensure all risk markers are visible on the map
- **Capture:** Full-page screenshot showing:
  - Map canvas with geospatial risk overlay (colors, markers)
  - Legend/layer toggles (risk zones, alert markers, etc.)
  - Any zoom/pan/filter controls
- **File:** `static/evidence/s3_06_map_desktop_overview.png`

**1.2 Map Legend & Toggle Panel**
- Show the legend panel in full (if it's a sidebar or popup)
- Toggle each overlay on/off to show interactivity
- **Capture:** Screenshot of the fully expanded legend with all category labels visible
- **File:** `static/evidence/s3_06_map_legend_desktop.png`

**1.3 Personalized Map (Authenticated User)**
- Log out and register a new test account
- Log in with that account
- Navigate to map and optionally set a home location / preferences
- **Capture:** Map with personalized styling or data (if applicable; if identical to guest, that's OK)
- **File:** `static/evidence/s3_06_map_authenticated_desktop.png`

**1.4 Map with Risk Polygon Overlay**
- If available, show a zoomed view of a specific risk zone or polygon
- **Capture:** Screenshot showing risk polygon detail
- **File:** `static/evidence/s3_06_map_risk_polygon_desktop.png` (or skip if N/A)

**1.5 Error/Fallback State (if testable)**
- If there's a way to trigger a fallback (e.g., disable backend, bad geojson)
- **Capture:** Screenshot of graceful fallback UI
- **File:** `static/evidence/s3_06_map_fallback_desktop.png` (or skip if N/A)

---

### Part 2: Mobile Screenshots (360px viewport)

**2.1 Map on Mobile — Full View**
- Open `http://127.0.0.1:8080/map.php` on a mobile device or browser at 360px width
- **Capture:** Screenshot showing:
  - Map canvas scaled to mobile width
  - Touch-friendly controls visible
  - No horizontal scroll or cutoff
- **File:** `static/evidence/s3_06_map_mobile_full.png`

**2.2 Mobile Map Controls & Legend**
- Show the legend/toggle panel on mobile
- Verify buttons and text are readable and tappable
- **Capture:** Screenshot of the legend in mobile view (may be a modal/drawer if responsive)
- **File:** `static/evidence/s3_06_map_mobile_legend.png`

**2.3 Mobile Map Accessibility (Screen Reader Readability)**
- Test with a screen reader or accessibility inspector (e.g., Chrome DevTools Accessibility pane)
- Verify map region has a label, buttons have names, etc.
- **Capture:** Screenshot of DevTools Accessibility tree showing map structure OR screenshot of screen reader labels (if visible)
- **File:** `static/evidence/s3_06_map_mobile_a11y.png`

**2.4 Mobile Zoom/Pan Interaction (preparation for video)**
- Perform a pinch-zoom or double-tap on map; pan left/right
- Note the interaction smoothness and whether legend follows
- **Note:** This will be part of the video walkthrough

---

### Part 3: Video Walkthrough (60–120 seconds)

**3.1 Video Recording Setup**
- Use OBS, screen capture software, or browser DevTools screen recorder
- Set viewport to 1280px (desktop) for clarity
- Ensure audio is clear (optional) or add subtitles/captions
- Target duration: 60–120 seconds

**3.2 Video Content (Recommended Flow)**

**Segment A: Map Overview & Legend (0–20 sec)**
- Start with the map fully loaded and zoomed to show multiple risk zones
- Show risk markers in different colors (high/medium/low)
- Click/interact with legend to toggle a layer off, then back on
- Demonstrate legend is readable and controls are responsive

**Segment B: Zoom & Pan Interactions (20–40 sec)**
- Zoom in on a specific area (double-click or scroll wheel)
- Pan left/right to show spatial context
- Zoom back out
- Demonstrate smooth interactions and no lag

**Segment C: Click Marker Interaction (40–60 sec)**
- Click on a risk marker or alert on the map
- Verify a popup or detail panel appears (if implemented)
- Show popup contents (e.g., alert name, severity, location)
- Close the popup

**Segment D: Fallback/Error Handling (60–90 sec, optional)**
- If there's a graceful fallback (e.g., when backend is slow), demonstrate it
- Show recovery to normal state
- OR show that the map remains usable even in low-network conditions

**Segment E: Mobile Responsiveness (90–120 sec, optional)**
- Quick switch to mobile view (360px)
- Show map is still usable and touch controls work
- Pinch-zoom on mobile (if testable via DevTools device emulation)

**3.3 Video File**
- **File:** `static/evidence/s3_06_map_walkthrough.mp4` (or `.webm`, `.mkv`)
- **Subtitles (optional):** If adding narration, keep it clear and concise

---

## File Placement & Verification

1. **Place all files in:** `static/evidence/`

2. **Expected file list after captures:**
   ```
   static/evidence/
   ├── s3_06_map_desktop_overview.png
   ├── s3_06_map_legend_desktop.png
   ├── s3_06_map_authenticated_desktop.png
   ├── s3_06_map_risk_polygon_desktop.png (optional)
   ├── s3_06_map_fallback_desktop.png (optional)
   ├── s3_06_map_mobile_full.png
   ├── s3_06_map_mobile_legend.png
   ├── s3_06_map_mobile_a11y.png
   ├── s3_06_map_walkthrough.mp4
   └── S3_CLOSEOUT_MANIFEST_2026-04-11.md (existing)
   ```

3. **Verify evidence is complete:**
   ```bash
   npm run verify:evidence:s3
   ```
   This command checks that required S3-06 files are present and valid.

4. **Update the S3 closeout manifest** if needed to document when captures were completed:
   ```bash
   # Edit static/evidence/S3_CLOSEOUT_MANIFEST_2026-04-11.md
   # and add a session entry with capture date and completion notes
   ```

---

## Accessibility & Quality Checklist

- [ ] Desktop screenshots are at 1280px and show full map + legend
- [ ] Mobile screenshots are at 360px and text is readable (no cutoff)
- [ ] Video is smooth (60fps if possible, at least 30fps)
- [ ] Video includes at least one interaction (zoom/pan/click)
- [ ] All files have descriptive names and are in `static/evidence/`
- [ ] `npm run verify:evidence:s3` passes with green checkmarks
- [ ] Files are committed and pushed to the branch

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Map shows no markers | Verify `npm run demo:setup` ran successfully; check backend logs for data load errors |
| Legend doesn't appear | May be hidden by design; use DevTools to inspect and take screenshot of DOM structure |
| Video is too large | Compress with ffmpeg: `ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4` |
| `npm run verify:evidence:s3` fails | Check file paths and naming; ensure all required files are in `static/evidence/` |
| Screenshot tool isn't working | Use OS screenshot utility (Windows: Snip & Sketch; macOS: Cmd+Shift+4; Linux: GNOME Screenshot) |

---

## Once Captures Are Complete

1. **Commit the evidence files:**
   ```bash
   git add static/evidence/
   git commit -m "docs(S3-06): Add manual evidence captures for Stage 3 map verification"
   ```

2. **Update TODO.md** to mark S3-06 as completed:
   ```bash
   # Edit docs/TODO.md and change S3-06 status to [x]
   ```

3. **Push to the PR branch:**
   ```bash
   git push origin <your-branch>
   ```

4. **Notify the team** that S3-06 evidence is ready for grading review.

---

**Questions?** Refer to [docs/PLANNING_DOCS/STAGE3_DOCS/STAGE3_VERIFICATION_EVIDENCE.md](../../../docs/PLANNING_DOCS/STAGE3_DOCS/STAGE3_VERIFICATION_EVIDENCE.md) for additional context on Stage 3 deliverables and verification criteria.
