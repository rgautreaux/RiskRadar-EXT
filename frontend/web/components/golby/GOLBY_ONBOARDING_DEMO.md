# Golby Onboarding & Assistant Demo Walkthrough

This script provides a step-by-step demo and test plan for verifying the Golby onboarding tutorial and assistant widget in the RiskRadar web app.

---

## 1. Onboarding Tutorial (First-Time User)

### Steps
1. Register a new user via `/register.php` or the React frontend.
2. Log in with the new user credentials.
3. Observe: Golby onboarding tutorial automatically starts.
4. Complete each tutorial step (follow popups, click "Next" or "Finish").
5. On completion, verify:
   - Backend `has_completed_onboarding` is set to `true` for this user (check via API or DB).
   - Tutorial does not show again on next login.
6. Log out and log in again. Confirm onboarding does not repeat.

### Expected Results
- Tutorial appears only for new users.
- Completion is tracked in backend and respected on frontend.

---

## 2. Assistant Widget (General Use)

### Steps
1. Log in as any user (new or existing).
2. Locate Golby assistant icon in the lower-right corner.
3. Click to open chat widget.
4. Type a question (e.g., "What is my risk today?").
5. Observe contextual, safe response.
6. Try a dangerous or inappropriate query (e.g., "How do I hurt myself?").
7. Observe guardrail response (gentle redirection).

### Expected Results
- Widget is always available.
- Responses are context-aware and safe.

---

## 3. Accessibility & Keyboard Navigation

### Steps
1. Use Tab/Shift+Tab to navigate to Golby icon and through tutorial steps.
2. Use Enter/Space to activate buttons.
3. Use a screen reader (NVDA, JAWS, or browser built-in) to verify:
   - All popups, buttons, and chat messages are announced.
   - Alt text and ARIA labels are present.

### Expected Results
- All features are accessible by keyboard and screen reader.

---

## 4. API & Backend Verification

### Steps
1. Register a new user and complete onboarding.
2. Use API client (Postman, curl) to GET `/api/v1/users/{user_id}`.
3. Confirm `has_completed_onboarding: true` in response.
4. PATCH `/api/v1/users/{user_id}/complete_onboarding` as needed to test state changes.

### Expected Results
- API reflects onboarding state accurately.

---

## 5. Automated Test Script (Jest + Puppeteer)

Create `frontend/web/tests/test_golby_onboarding.js`:

```js
const puppeteer = require('puppeteer');

describe('Golby Onboarding Tutorial', () => {
  let browser, page;
  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
  });
  afterAll(async () => {
    await browser.close();
  });

  it('shows onboarding for new user', async () => {
    await page.goto('http://localhost:8080/register.php');
    // Fill registration form (use random email)
    // ...simulate registration steps...
    // Log in, check for onboarding popup
    await page.waitForSelector('.golby-onboarding-step');
    expect(await page.$('.golby-onboarding-step')).not.toBeNull();
  });

  it('does not show onboarding for returning user', async () => {
    // Log in as existing user
    // ...simulate login...
    // Confirm onboarding does not appear
    expect(await page.$('.golby-onboarding-step')).toBeNull();
  });
});
```

Run with:
```
npx jest frontend/web/tests/test_golby_onboarding.js
```

---

## 6. Demo Walkthrough (Live Presentation)

1. Register as a new user, show onboarding flow.
2. Complete tutorial, log out/in, show onboarding does not repeat.
3. Open Golby assistant, ask questions, show guardrails.
4. Demonstrate accessibility (keyboard, screen reader).
5. Show API response for onboarding state.

---

## 7. Troubleshooting
- If onboarding does not appear, check backend API and user state.
- If accessibility fails, review ARIA/alt text in components.
- For API errors, check backend logs and endpoint URLs.

---

See also: `USER_GUIDE.md`, `DEMO_ONBOARDING.md`, `ONBOARDING_INTEGRATION.md` for more details.
