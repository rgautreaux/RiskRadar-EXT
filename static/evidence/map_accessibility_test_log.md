# Map and Accessibility Test Log - Stage 3 Closeout

This checklist is the execution guide for S3-06 artifact capture.
All files must be created at the exact paths below for verifier success.

## Verifier-Gated Artifact Paths (Required)

- [ ] static/evidence/s3-map-desktop-overlays.png
- [ ] static/evidence/s3-map-desktop-controls-legend.png
- [ ] static/evidence/s3-map-desktop-personalized.png
- [ ] static/evidence/s3-map-mobile-layout.png
- [ ] static/evidence/s3-map-mobile-controls.png
- [ ] static/evidence/s3-map-walkthrough.mp4
- [ ] static/evidence/s3-map-keyboard-nav.mp4

## Capture Procedure

1. Start backend API and web frontend.
2. Open the map page in desktop viewport (1280px).
3. Capture desktop screenshots:
	- overlays active
	- controls plus legend visible
	- personalized mode enabled with user ID
4. Switch to mobile viewport (360px) and capture:
	- responsive map layout
	- mobile-friendly controls and toggles
5. Record walkthrough video (30 to 60 seconds):
	- load map
	- zoom and pan
	- toggle at least one overlay
	- show fallback or empty-state handling
6. Record keyboard navigation video:
	- Tab through filter, toggles, and map region
	- Enter or Space activation on controls
	- Escape to close modal where applicable

## Manual Accessibility Acceptance

- [ ] Overlay toggles, region filter, and user ID input are keyboard accessible
- [ ] Map container is focusable and responds to keyboard pan and zoom keys
- [ ] Marker details dialog is reachable and closable with Escape
- [ ] Toast and feedback text are announced through live region behavior
- [ ] Color and icon cues remain understandable at desktop and mobile sizes
- [ ] Fallback message appears on backend/network failure

## Final Validation

Run this command from repository root:

npm run verify:evidence:s3

Pass condition:
- Output ends with PASS: S3-06 artifacts and links are complete.

---
Assigned to: Max
Updated by: GitHub Copilot
Date: 2026-04-11
