# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: demo-journey.spec.js >> guest -> register -> alerts -> assistant flow
- Location: frontend\web\tests\e2e\demo-journey.spec.js:13:1

# Error details

```
Error: page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:8080/login.php
Call log:
  - navigating to "http://127.0.0.1:8080/login.php", waiting until "domcontentloaded"

```

# Test source

```ts
  1  | const { test, expect } = require('@playwright/test');
  2  | 
  3  | const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';
  4  | 
  5  | function uniqueIdentity() {
  6  |   const id = Date.now();
  7  |   return {
  8  |     email: `playwright_user_${id}@example.com`,
  9  |     password: 'PlaywrightPass123!'
  10 |   };
  11 | }
  12 | 
  13 | test('guest -> register -> alerts -> assistant flow', async ({ page }) => {
  14 |   const identity = uniqueIdentity();
  15 | 
> 16 |   await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
     |              ^ Error: page.goto: net::ERR_CONNECTION_REFUSED at http://127.0.0.1:8080/login.php
  17 |   await page.getByRole('button', { name: /continue as guest/i }).click();
  18 |   await expect(page).toHaveURL(/index\.php/);
  19 | 
  20 |   await page.goto(`${WEB_BASE}/logout.php`, { waitUntil: 'domcontentloaded' });
  21 |   await expect(page).toHaveURL(/login\.php/);
  22 | 
  23 |   await page.goto(`${WEB_BASE}/register.php`, { waitUntil: 'domcontentloaded' });
  24 |   await page.fill('input[name="display_name"]', 'Playwright User');
  25 |   await page.fill('input[name="email"]', identity.email);
  26 |   await page.fill('input[name="password"]', identity.password);
  27 |   await page.fill('input[name="zip_code"]', '70808');
  28 | 
  29 |   await Promise.all([
  30 |     page.waitForURL(/login\.php/),
  31 |     page.getByRole('button', { name: /create my riskradar account/i }).click()
  32 |   ]);
  33 | 
  34 |   await page.fill('input[name="email"]', identity.email);
  35 |   await page.fill('input[name="password"]', identity.password);
  36 |   await Promise.all([
  37 |     page.waitForURL(/index\.php/),
  38 |     page.getByRole('button', { name: /sign in/i }).click()
  39 |   ]);
  40 | 
  41 |   await page.goto(`${WEB_BASE}/alerts.php`, { waitUntil: 'domcontentloaded' });
  42 |   await expect(page).toHaveURL(/alerts\.php/);
  43 |   await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  44 | 
  45 |   await page.goto(`${WEB_BASE}/assistant.php`, { waitUntil: 'domcontentloaded' });
  46 |   await expect(page.locator('#riskradar-ai-assistant-widget')).toBeVisible();
  47 | 
  48 |   const openButton = page.getByRole('button', { name: /open golby ai assistant/i });
  49 |   await openButton.waitFor({ timeout: 20000 });
  50 |   await openButton.click();
  51 | 
  52 |   const messageInput = page.getByRole('textbox', { name: /message input/i });
  53 |   await messageInput.waitFor({ timeout: 20000 });
  54 |   await messageInput.fill('What are the highest alerts right now?');
  55 |   await page.getByRole('button', { name: /send message/i }).click();
  56 | 
  57 |   await expect(page.getByRole('button', { name: /this was helpful/i }).first()).toBeVisible({ timeout: 20000 });
  58 | });
  59 | 
```