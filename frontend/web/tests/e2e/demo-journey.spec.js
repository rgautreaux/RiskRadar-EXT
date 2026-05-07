const { test, expect } = require('@playwright/test');

const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';

function uniqueIdentity() {
  const id = Date.now();
  return {
    email: `playwright_user_${id}@example.com`,
    password: 'PlaywrightPass123!'
  };
}

test('guest -> register -> alerts -> assistant flow', async ({ page }) => {
  const identity = uniqueIdentity();

  await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: /continue as guest/i }).click();
  await expect(page).toHaveURL(/index\.php/);

  await page.goto(`${WEB_BASE}/logout.php`, { waitUntil: 'domcontentloaded' });
  await expect(page).toHaveURL(/login\.php/);

  await page.goto(`${WEB_BASE}/register.php`, { waitUntil: 'domcontentloaded' });
  await page.fill('input[name="display_name"]', 'Playwright User');
  await page.fill('input[name="email"]', identity.email);
  await page.fill('input[name="password"]', identity.password);
  await page.fill('input[name="zip_code"]', '70808');

  await Promise.all([
    page.waitForURL(/login\.php/),
    page.getByRole('button', { name: /create my riskradar account/i }).click()
  ]);

  await page.fill('input[name="email"]', identity.email);
  await page.fill('input[name="password"]', identity.password);
  await Promise.all([
    page.waitForURL(/index\.php/),
    page.getByRole('button', { name: /sign in/i }).click()
  ]);

  await page.goto(`${WEB_BASE}/alerts.php`, { waitUntil: 'domcontentloaded' });
  await expect(page).toHaveURL(/alerts\.php/);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();

  await page.goto(`${WEB_BASE}/assistant.php`, { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#riskradar-ai-assistant-widget')).toBeVisible();

  const openButton = page.getByRole('button', { name: /open golby ai assistant/i });
  await openButton.waitFor({ timeout: 20000 });
  await openButton.click();

  const messageInput = page.getByRole('textbox', { name: /message input/i });
  await messageInput.waitFor({ timeout: 20000 });
  await messageInput.fill('What are the highest alerts right now?');
  await page.getByRole('button', { name: /send message/i }).click();

  await expect(page.getByRole('button', { name: /this was helpful/i }).first()).toBeVisible({ timeout: 20000 });
});
