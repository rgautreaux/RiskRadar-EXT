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
  await expect(page.locator('#riskradar-assistant-page-welcome, #riskradar-ai-assistant-widget').first()).toBeVisible();

  const openButton = page.getByRole('button', { name: /open golby ai assistant/i });
  await openButton.waitFor({ timeout: 20000 });
  await openButton.click({ force: true });

  // Wait for the message input to appear (may be in an iframe or shadow DOM)
  // Look for input with placeholder or other chat-related selectors
  await page.waitForTimeout(2000); // Give widget time to initialize
  
  const messageInput = page.locator('input[placeholder*="message"], textarea, [role="textbox"]').first();
  await expect(messageInput).toBeVisible({ timeout: 10000 });
  
  // Verify helpful feedback button appears after interaction
  await expect(page.getByRole('button', { name: /this was helpful|helpful/i }).first()).toBeVisible({ timeout: 20000 });
});
