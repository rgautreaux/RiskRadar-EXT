# Stage 3 Evidence Closeout Manifest (S3-06)

Date prepared: 2026-04-11  
Status: Ready for manual capture and filing

## Required artifacts

### Desktop captures (1280px)
- [ ] `s3-map-desktop-overlays.png`  
  Description: map with live alert and risk overlays visible
- [ ] `s3-map-desktop-controls-legend.png`  
  Description: overlay toggle controls and legend expanded
- [ ] `s3-map-desktop-personalized.png`  
  Description: personalized mode enabled with user id shown

### Mobile captures (360px)
- [ ] `s3-map-mobile-layout.png`  
  Description: responsive map layout at 360px
- [ ] `s3-map-mobile-controls.png`  
  Description: responsive overlay controls at 360px

### Video walkthrough
- [ ] `s3-map-walkthrough.mp4` (or `.webm`)  
  Description: 30-60 second flow: load -> pan/zoom -> overlay toggle -> fallback/error state

### Accessibility proof
- [ ] `s3-map-keyboard-nav.mp4` (or `.webm`)  
  Description: keyboard-only tab/enter interaction with controls and map

## Capture checklist
1. Set viewport to 1280px for desktop shots.
2. Set viewport to 360px for mobile shots.
3. Ensure timestamp and URL bar context are visible when practical.
4. Verify overlays/data are live before screenshot capture.
5. Save all artifacts under `static/evidence/` with exact filenames above.

## Filing checklist
- [ ] Add links to all artifacts in `docs/PLANNING_DOCS/STAGE3_DOCS/STAGE3_VERIFICATION_EVIDENCE.md`
- [ ] Mark S3-06 and evidence checklist items complete in `docs/TODO.md`
- [ ] Add one-line note in `README.md` or `docs/STAGES.md` indicating S3 evidence bundle captured
