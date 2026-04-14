# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend\web\tests\access_restriction.spec.js >> Authenticated User Access >> User can access personalized map controls
- Location: frontend\web\tests\access_restriction.spec.js:71:3

# Error details

```
Error: expect(page).toHaveURL(expected) failed

Expected pattern: /index\.php/
Received string:  "http://localhost:8080/login.php"
Timeout: 5000ms

Call log:
  - Expect "toHaveURL" with timeout 5000ms
    9 × unexpected value "http://localhost:8080/login.php"

```

# Page snapshot

```yaml
- generic [ref=e2]:
  - banner [ref=e3]:
    - generic [ref=e4]:
      - paragraph [ref=e5]: CMPS 357 Web Extension
      - link "RiskRadar Web" [ref=e6] [cursor=pointer]:
        - /url: index.php
    - navigation "Primary navigation" [ref=e7]:
      - link "Login Icon Login" [ref=e8] [cursor=pointer]:
        - /url: login.php
        - img "Login Icon" [ref=e9]
        - text: Login
      - link "Register Icon Sign Up" [ref=e10] [cursor=pointer]:
        - /url: register.php
        - img "Register Icon" [ref=e11]
        - text: Sign Up
  - main [ref=e12]:
    - article [ref=e14]:
      - generic [ref=e16]:
        - paragraph [ref=e17]: Account access
        - heading "Sign in to RiskRadar" [level=1] [ref=e18]
      - paragraph [ref=e20]: Login failed. Please verify the backend is running and try again.
      - generic [ref=e21]:
        - generic [ref=e22]:
          - generic [ref=e23]: Email
          - textbox "Email" [ref=e24]: demo_low@riskradar.local
        - generic [ref=e25]:
          - generic [ref=e26]: Password
          - textbox "Password" [ref=e27]
        - generic [ref=e28]:
          - generic [ref=e29]: ZIP code (optional)
          - textbox "ZIP code (optional)" [ref=e30]
        - button "Sign in" [ref=e31] [cursor=pointer]
      - button "Continue as Guest" [ref=e33] [cursor=pointer]
      - paragraph [ref=e34]:
        - text: Don’t have an account?
        - link "Create one" [ref=e35] [cursor=pointer]:
          - /url: register.php
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
  15 |     await page.click('button[name="action"][value="guest"]');
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
> 48 |     await expect(page).toHaveURL(/index\.php/);
     |                        ^ Error: expect(page).toHaveURL(expected) failed
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