# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend\web\tests\access_restriction.spec.js >> Authenticated User Access >> User can access smart alerts
- Location: frontend\web\tests\access_restriction.spec.js:49:3

# Error details

```
Test timeout of 30000ms exceeded while running "beforeEach" hook.
```

```
Error: page.fill: Test timeout of 30000ms exceeded.
Call log:
  - waiting for locator('input[name="email"]')

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
  8  |   await expect(page.locator('.warning-panel, .empty-state')).toContainText(expectedText);
  9  | }
  10 | 
  11 | test.describe('Guest Access Restriction', () => {
  12 |   test('Guest is blocked from risk page', async ({ page }) => {
  13 |     await expectGuestLockout(page, '/risk.php', 'Guest mode: Personalized risk scoring is only available to registered users');
  14 |   });
  15 | 
  16 |   test('Guest is blocked from smart alerts', async ({ page }) => {
  17 |     await expectGuestLockout(page, '/smart_alerts.php', 'Guest mode: Prioritized alerts are only available to registered users');
  18 |   });
  19 | 
  20 |   test('Guest is blocked from profile', async ({ page }) => {
  21 |     await expectGuestLockout(page, '/profile.php', 'Guest mode: Profile management is only available to registered users');
  22 |   });
  23 | 
  24 |   test('Guest is blocked from forecast', async ({ page }) => {
  25 |     await expectGuestLockout(page, '/forecast.php', 'Guest mode: Forecasting is only available to registered users');
  26 |   });
  27 | 
  28 |   test('Guest is shown map overlay lockout', async ({ page }) => {
  29 |     await page.goto(`${BASE_URL}/map.php`);
  30 |     await expect(page.locator('.warning-panel, .empty-state')).toContainText('Guest mode: Personalized map overlays and controls are only available to registered users');
  31 |   });
  32 | });
  33 | 
  34 | test.describe('Authenticated User Access', () => {
  35 |   test.beforeEach(async ({ page }) => {
  36 |     // Log in as a test user (assumes a test user exists)
  37 |     await page.goto(`${BASE_URL}/login.php`);
> 38 |     await page.fill('input[name="email"]', 'testuser@example.com');
     |                ^ Error: page.fill: Test timeout of 30000ms exceeded.
  39 |     await page.fill('input[name="password"]', 'testpassword');
  40 |     await page.click('button[type="submit"]');
  41 |     await expect(page).toHaveURL(/profile\.php/);
  42 |   });
  43 | 
  44 |   test('User can access risk page', async ({ page }) => {
  45 |     await page.goto(`${BASE_URL}/risk.php`);
  46 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  47 |   });
  48 | 
  49 |   test('User can access smart alerts', async ({ page }) => {
  50 |     await page.goto(`${BASE_URL}/smart_alerts.php`);
  51 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  52 |   });
  53 | 
  54 |   test('User can access profile', async ({ page }) => {
  55 |     await page.goto(`${BASE_URL}/profile.php`);
  56 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  57 |   });
  58 | 
  59 |   test('User can access forecast', async ({ page }) => {
  60 |     await page.goto(`${BASE_URL}/forecast.php`);
  61 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  62 |   });
  63 | 
  64 |   test('User can access personalized map controls', async ({ page }) => {
  65 |     await page.goto(`${BASE_URL}/map.php`);
  66 |     await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  67 |   });
  68 | });
  69 | 
```