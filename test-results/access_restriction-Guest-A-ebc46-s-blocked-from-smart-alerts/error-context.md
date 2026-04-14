# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: access_restriction.spec.js >> Guest Access Restriction >> Guest is blocked from smart alerts
- Location: frontend\web\tests\access_restriction.spec.js:23:3

# Error details

```
Test timeout of 60000ms exceeded while running "beforeEach" hook.
```

```
Error: page.click: Test timeout of 60000ms exceeded.
Call log:
  - waiting for locator('button[name="action"][value="guest"]')

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - heading "Not Found" [level=1] [ref=e2]
  - paragraph [ref=e3]:
    - text: The requested resource
    - code [ref=e4]: /login.php
    - text: was not found on this server.
```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | const BASE_URL = 'http://localhost:8080';
  4  | 
  5  | // Helper: Go to a page and return guest lockout message selector
  6  | async function expectGuestLockout(page, path, expectedText) {
  7  |   await page.goto(`${BASE_URL}${path}`);
  8  |   await expect(page.locator('.warning-panel').first()).toContainText(expectedText);
  9  | }
  10 | 
  11 | test.describe('Guest Access Restriction', () => {
  12 |   test.beforeEach(async ({ page }) => {
  13 |     // Go to login and click "Continue as Guest" to set guest mode
  14 |     await page.goto(`${BASE_URL}/login.php`);
> 15 |     await page.click('button[name="action"][value="guest"]');
     |                ^ Error: page.click: Test timeout of 60000ms exceeded.
  16 |     // Should redirect to index.php, but session is now guest
  17 |   });
  18 | 
  19 |   test('Guest is blocked from risk page', async ({ page }) => {
  20 |     await expectGuestLockout(page, '/risk.php', 'Guest mode: Personalized risk scoring is only available to registered users');
  21 |   });
  22 | 
  23 |   test('Guest is blocked from smart alerts', async ({ page }) => {
  24 |     await expectGuestLockout(page, '/smart_alerts.php', 'Guest mode: Prioritized alerts are only available to registered users');
  25 |   });
  26 | 
  27 |   test('Guest is blocked from profile', async ({ page }) => {
  28 |     await expectGuestLockout(page, '/profile.php', 'Guest mode: Profile management is only available to registered users');
  29 |   });
  30 | 
  31 |   test('Guest is blocked from forecast', async ({ page }) => {
  32 |     await expectGuestLockout(page, '/forecast.php', 'Guest mode: Forecasting is only available to registered users');
  33 |   });
  34 | 
  35 |   test('Guest is shown map overlay lockout', async ({ page }) => {
  36 |     await page.goto(`${BASE_URL}/map.php`);
  37 |     await expect(page.locator('.warning-panel')).toContainText('Guest mode: Personalized map overlays and controls are only available to registered users');
  38 |   });
  39 | });
  40 | 
  41 | test.describe('Authenticated User Access', () => {
  42 |   test.beforeEach(async ({ page }) => {
  43 |     // Log in as a seeded demo user
  44 |     await page.goto(`${BASE_URL}/login.php`);
  45 |     await page.fill('input[name="email"]', 'demo_low@riskradar.local');
  46 |     await page.fill('input[name="password"]', 'DemoLow123!');
  47 |     await page.click('button[type="submit"]');
  48 |     await expect(page).toHaveURL(/index\.php/);
  49 |   });
  50 | 
  51 |   test('User can access risk page', async ({ page }) => {
  52 |     await page.goto(`${BASE_URL}/risk.php`);
  53 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  54 |   });
  55 | 
  56 |   test('User can access smart alerts', async ({ page }) => {
  57 |     await page.goto(`${BASE_URL}/smart_alerts.php`);
  58 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  59 |   });
  60 | 
  61 |   test('User can access profile', async ({ page }) => {
  62 |     await page.goto(`${BASE_URL}/profile.php`);
  63 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  64 |   });
  65 | 
  66 |   test('User can access forecast', async ({ page }) => {
  67 |     await page.goto(`${BASE_URL}/forecast.php`);
  68 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  69 |   });
  70 | 
  71 |   test('User can access personalized map controls', async ({ page }) => {
  72 |     await page.goto(`${BASE_URL}/map.php`);
  73 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  74 |   });
  75 | });
  76 | 
```