# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: frontend\web\tests\access_restriction.spec.js >> Guest Access Restriction >> Guest is shown map overlay lockout
- Location: frontend\web\tests\access_restriction.spec.js:35:3

# Error details

```
Error: expect(locator).toContainText(expected) failed

Locator: locator('.warning-panel, .empty-state')
Expected substring: "Guest mode: Personalized map overlays and controls are only available to registered users"
Error: strict mode violation: locator('.warning-panel, .empty-state') resolved to 2 elements:
    1) <section class="panel warning-panel">…</section> aka locator('section').filter({ hasText: 'Guest mode: Personalized map' })
    2) <p class="empty-state">…</p> aka getByText('Guest mode: Personalized map')

Call log:
  - Expect "toContainText" with timeout 5000ms
  - waiting for locator('.warning-panel, .empty-state')

```

# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - paragraph [ref=e3]:
    - text: "Guest mode: Personalized map overlays and controls are only available to registered users."
    - link "Sign in" [ref=e4] [cursor=pointer]:
      - /url: login.php
    - text: or
    - link "create an account" [ref=e5] [cursor=pointer]:
      - /url: register.php
    - text: for full access.
  - generic [ref=e6]:
    - banner [ref=e7]:
      - generic [ref=e8]:
        - paragraph [ref=e9]: CMPS 357 Web Extension
        - link "RiskRadar Web" [ref=e10] [cursor=pointer]:
          - /url: index.php
        - paragraph [ref=e11]: Guest mode enabled
      - navigation "Primary navigation" [ref=e12]:
        - link "Dashboard Icon Dashboard" [ref=e13] [cursor=pointer]:
          - /url: index.php
          - img "Dashboard Icon" [ref=e14]
          - text: Dashboard
        - link "Alerts Icon Alerts" [ref=e15] [cursor=pointer]:
          - /url: alerts.php
          - img "Alerts Icon" [ref=e16]
          - text: Alerts
        - link "Summaries Icon Summaries" [ref=e17] [cursor=pointer]:
          - /url: summaries.php
          - img "Summaries Icon" [ref=e18]
          - text: Summaries
        - link "Profile Icon Profile" [ref=e19] [cursor=pointer]:
          - /url: profile.php
          - img "Profile Icon" [ref=e20]
          - text: Profile
        - link "Risk Icon Risk" [ref=e21] [cursor=pointer]:
          - /url: risk.php
          - img "Risk Icon" [ref=e22]
          - text: Risk
        - link "Map Icon Map" [ref=e23] [cursor=pointer]:
          - /url: map.php
          - img "Map Icon" [ref=e24]
          - text: Map
        - link "Forecast Icon Forecast" [ref=e25] [cursor=pointer]:
          - /url: forecast.php
          - img "Forecast Icon" [ref=e26]
          - text: Forecast
        - link "Assistant Icon Assistant" [ref=e27] [cursor=pointer]:
          - /url: assistant.php
          - img "Assistant Icon" [ref=e28]
          - text: Assistant
        - link "Login Icon Sign In" [ref=e29] [cursor=pointer]:
          - /url: login.php
          - img "Login Icon" [ref=e30]
          - text: Sign In
    - main [ref=e31]:
      - generic [ref=e32]:
        - generic [ref=e33]:
          - paragraph [ref=e34]: Stage 3 scaffold
          - heading "Interactive Risk Map" [level=1] [ref=e35]
        - paragraph [ref=e36]: This page is reserved for the Stage 3 interactive map extension (Plotly), including zoom/pan support and click-through risk details.
      - generic [ref=e37]:
        - heading "Interactive Map" [level=2] [ref=e38]
        - generic [ref=e39]:
          - generic [ref=e40]: "Region Filter:"
          - combobox "Region Filter" [ref=e41]:
            - option "All Regions" [selected]
            - option "Louisiana"
            - option "Texas"
            - option "Mississippi"
          - generic [ref=e42]: "Select a region to filter map overlays. Use Tab to move to overlays and toggles. Shortcut: Alt+R."
        - generic [ref=e43]:
          - generic [ref=e44]: "User ID for Personalized Map:"
          - spinbutton "User ID for Personalized Map" [ref=e45]: "1"
          - generic [ref=e46]: "Enter your numeric user ID to enable personalized risk overlays. This is required for personalized map mode. Shortcut: Alt+U."
        - group "Overlay Toggles" [ref=e47]:
          - generic [ref=e48]: "Toggle overlays with Space or Enter. Keyboard shortcuts: Alt+1 Alerts, Alt+2 Risk Zones, Alt+3 AQI, Alt+4 Wildfire, Alt+5 Earthquake, Alt+6 Weather, Alt+7 Pollution."
          - generic [ref=e49]:
            - checkbox "Show Alerts" [checked] [ref=e50]
            - text: Show Alerts
          - generic [ref=e51]:
            - checkbox "Show Risk Zones" [checked] [ref=e52]
            - text: Show Risk Zones
          - generic [ref=e53]:
            - checkbox "AQI Overlay" [ref=e54]
            - text: AQI Overlay
          - generic [ref=e55]:
            - checkbox "Wildfire Overlay" [ref=e56]
            - text: Wildfire Overlay
          - generic [ref=e57]:
            - checkbox "Earthquake Overlay" [ref=e58]
            - text: Earthquake Overlay
          - generic [ref=e59]:
            - checkbox "Weather Overlay" [ref=e60]
            - text: Weather Overlay
          - generic [ref=e61]:
            - checkbox "Pollution Overlay" [ref=e62]
            - text: Pollution Overlay
        - generic [ref=e63]:
          - generic [ref=e64]:
            - checkbox "Personalized Risk Map" [ref=e65]
            - text: Personalized Risk Map
          - button "Toggle dark mode" [ref=e66] [cursor=pointer]: 🌙 Dark Mode
          - button "How to use this map" [ref=e67] [cursor=pointer]: Help
  - region "Risk map showing alerts and risk zones. Use arrow keys to pan. Press Enter or Space on a marker for details." [ref=e68]:
    - application "Interactive risk map with overlays and markers" [ref=e69]
    - generic [ref=e71]:
      - status "Loading" [ref=e72]
      - generic [ref=e73]: Loading map data...
    - generic [ref=e75]: Use Tab to focus the map. Use arrow keys to pan. Press Enter or Space on a marker for details. All overlays and controls are accessible by keyboard and screen reader. Markers and overlays are announced to assistive technology.
  - generic [ref=e76]:
    - button "Legend" [expanded] [ref=e77] [cursor=pointer]:
      - generic [ref=e78]: ▼
      - text: Legend
    - list [ref=e79]:
      - listitem [ref=e80]:
        - generic "High Alert" [ref=e81]:
          - img [ref=e82]
        - text: High severity alert (contrast checked)
      - listitem [ref=e84]:
        - generic "Medium Alert" [ref=e85]:
          - img [ref=e86]
        - text: Medium severity alert (contrast checked)
      - listitem [ref=e88]:
        - generic "Low Alert" [ref=e89]:
          - img [ref=e90]
        - text: Low severity alert (contrast checked)
      - listitem [ref=e92]:
        - generic "Extreme/High Risk" [ref=e93]:
          - img [ref=e94]
        - text: Extreme/High risk zone (contrast checked)
      - listitem [ref=e96]:
        - generic "Medium Risk" [ref=e97]:
          - img [ref=e98]
        - text: Medium risk zone (contrast checked)
      - listitem [ref=e100]:
        - generic "Low Risk" [ref=e101]:
          - img [ref=e102]
        - text: Low risk zone (contrast checked)
      - listitem [ref=e104]:
        - generic "AQI Overlay" [ref=e105]:
          - img [ref=e106]
        - text: AQI (Air Quality) overlay
      - listitem [ref=e108]:
        - generic "Wildfire Overlay" [ref=e109]:
          - img [ref=e110]
        - text: Wildfire overlay
      - listitem [ref=e112]:
        - generic "Earthquake Overlay" [ref=e113]:
          - img [ref=e114]
        - text: Earthquake overlay
      - listitem [ref=e116]:
        - generic "Weather Overlay" [ref=e117]:
          - img [ref=e118]
        - text: Weather overlay
      - listitem [ref=e120]:
        - generic "Pollution Overlay" [ref=e121]:
          - img [ref=e122]
        - text: Pollution overlay
    - generic [ref=e125]: All map overlays and controls are accessible by keyboard and screen reader. Colors have been checked for sufficient contrast. If you have difficulty distinguishing overlays, contact support for alternative patterns.
  - paragraph [ref=e126]: The map will display live alert markers and risk overlays as data becomes available. All features are keyboard and screen reader accessible. Focus indicators are visible for all controls.
  - generic [ref=e127]:
    - tooltip "Need help? Ask Golby!" [ref=e128]:
      - paragraph [ref=e129]: Need help? Ask Golby!
      - button "Dismiss tooltip" [ref=e130]: ×
    - button "Open Golby AI Assistant" [ref=e132]:
      - img "Golby the assistant looking waving" [ref=e133]:
        - img
      - generic [ref=e134]: Open Golby AI Assistant
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
> 37 |     await expect(page.locator('.warning-panel, .empty-state')).toContainText('Guest mode: Personalized map overlays and controls are only available to registered users');
     |                                                                ^ Error: expect(locator).toContainText(expected) failed
  38 |   });
  39 | });
  40 | 
  41 | test.describe('Authenticated User Access', () => {
  42 |   test.beforeEach(async ({ page }) => {
  43 |     // Log in as a test user (assumes a test user exists)
  44 |     await page.goto(`${BASE_URL}/login.php`);
  45 |     await page.fill('input[name="email"]', 'testuser@example.com');
  46 |     await page.fill('input[name="password"]', 'testpassword');
  47 |     await page.click('button[type="submit"]');
  48 |     await expect(page).toHaveURL(/profile\.php/);
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