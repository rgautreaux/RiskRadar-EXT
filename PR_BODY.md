Title: UI: Guest lockout + onboarding polish (accessible dialog, icons, Help trigger)

Summary
-------
This PR polishes the web frontend UI for guest lockout states and the Golby onboarding entry point. Changes are UI-only and do not modify backend logic or APIs.

Files changed
-------------
- `frontend/web/views/smart_alerts.php`
- `frontend/web/views/profile.php`
- `frontend/web/views/forecast.php`
- `frontend/web/views/risk.php`
- `frontend/web/public/assets/app.css`
- `frontend/web/components/golby/GolbyAssistantWidget.tsx`
- `frontend/web/components/layout.php`

What I changed
--------------
- Replaced emoji lockout indicators with consistent SVG icons (`warning.svg`, `info.svg`).
- Added an accessible, modal lockout dialog with focus management and Esc-to-close behavior.
- Added non-modal inline info tooltip for brief explanations about lockouts.
- Exposed a global onboarding opener (`window.openGolbyOnboarding`) and a custom event listener `golby:show-onboarding` so UI buttons can trigger onboarding.
- Added a `Help` button in the site header to trigger onboarding.
- Added CSS for lockout overlays, inline info, and modal dialog styles.
- Fixed asset paths to use `assets/icons/...`.

Accessibility notes
-------------------
- Dialogs use `role="dialog"` and `aria-modal="true"`.
- Interactive controls include `aria-label` or `aria-describedby` where appropriate.
- Focus moves to a logical control when the dialog opens and returns to the prior element on close.
- `Esc` closes the modal dialog.

Manual verification steps (smoke test)
------------------------------------
1. Create and push a branch locally (commands below), then serve static files to preview.

2. Serve the frontend locally (example using PHP built-in server):
```bash
php -S 127.0.0.1:8000 -t frontend/web/public
```

3. Open the following pages in your browser as a guest (not signed in):
   - http://127.0.0.1:8000/smart_alerts.php
   - http://127.0.0.1:8000/profile.php
   - http://127.0.0.1:8000/forecast.php
   - http://127.0.0.1:8000/risk.php

4. Verify behavior:
   - Lockout overlay displays with warning icon and clear messaging.
   - Clicking the locked form or buttons opens the modal dialog (or inline info when clicking the info button).
   - `Esc` closes the dialog and focus returns to the previous element.
   - `Tab` reaches Sign In / Create Account links and header Help button.
   - Header `Help` triggers the Golby onboarding; `/#onboard` also opens onboarding.

Git commands to create the branch, commit, and push
--------------------------------------------------
```bash
git checkout -b ui/lockout-onboarding-polish
git add frontend/web/views/smart_alerts.php frontend/web/views/profile.php frontend/web/views/forecast.php frontend/web/views/risk.php frontend/web/public/assets/app.css frontend/web/components/golby/GolbyAssistantWidget.tsx frontend/web/components/layout.php PR_BODY.md
git commit -m "UI: polish guest lockout + onboarding — accessible dialog, icons, Help trigger"
git push -u origin ui/lockout-onboarding-polish
```

PR body checklist
-----------------
- [ ] Title and description match this file
- [ ] Screenshots/GIFs attached showing dialog and onboarding
- [ ] Manual verification steps completed by reviewer
- [ ] Accessibility notes reviewed

Rollback plan
-------------
- Revert the branch or close PR. Changes are isolated to frontend UI files only.

Follow-ups (separate PRs recommended)
-----------------------------------
- Add Lighthouse/axe accessibility checks to CI.
- Add visual regression tests for the onboarding and lockout screens.

Contact/Notes
-------------
If you want I can also create a small `SMOKE_TEST.md` with copy/paste checks or add a minimal PR template. Reply with A (create `SMOKE_TEST.md`) or B (skip).
