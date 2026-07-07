const { test, expect } = require('@playwright/test');

const BASE_URL = 'http://riskradar.local';

// Helper: Go to a page and return guest lockout message selector
async function expectGuestLockout(page, path, expectedText) {
  await page.goto(`${BASE_URL}${path}`);
  await expect(page.locator('.warning-panel').first()).toContainText(expectedText);
}

test.describe('Guest Access Restriction', () => {
  test.beforeEach(async ({ page }) => {
    // Go to login and click "Continue as Guest" to set guest mode
    await page.goto(`${BASE_URL}/login.php`);
    await page.click('button[name="action"][value="guest"]');
    // Should redirect to index.php, but session is now guest
  });

  test('Guest is blocked from risk page', async ({ page }) => {
    await expectGuestLockout(page, '/risk.php', 'Guest mode: Personalized risk scoring is only available to registered users');
  });

  test('Guest is blocked from smart alerts', async ({ page }) => {
    await expectGuestLockout(page, '/smart_alerts.php', 'Guest mode: Prioritized alerts are only available to registered users');
  });

  test('Guest is blocked from profile', async ({ page }) => {
    await expectGuestLockout(page, '/profile.php', 'Guest mode: Profile management is only available to registered users');
  });

  test('Guest is blocked from forecast', async ({ page }) => {
    await expectGuestLockout(page, '/forecast.php', 'Guest mode: Forecasting is only available to registered users');
  });

  test('Guest is shown map overlay lockout', async ({ page }) => {
    await page.goto(`${BASE_URL}/map.php`);
    await expect(page.locator('.warning-panel')).toContainText('Guest mode: Personalized map overlays and controls are only available to registered users');
  });
});

test.describe('Authenticated User Access', () => {
  test.beforeEach(async ({ page }) => {
    // Log in as a seeded demo user
    await page.goto(`${BASE_URL}/login.php`);
    await page.fill('input[name="email"]', 'demo_low@riskradar.local');
    await page.fill('input[name="password"]', 'DemoLow123!');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL(/index\.php/);
  });

  test('User can access risk page', async ({ page }) => {
    await page.goto(`${BASE_URL}/risk.php`);
    await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  });

  test('User can access smart alerts', async ({ page }) => {
    await page.goto(`${BASE_URL}/smart_alerts.php`);
    await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  });

  test('User can access profile', async ({ page }) => {
    await page.goto(`${BASE_URL}/profile.php`);
    await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  });

  test('User can access forecast', async ({ page }) => {
    await page.goto(`${BASE_URL}/forecast.php`);
    await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  });

  test('User can access personalized map controls', async ({ page }) => {
    await page.goto(`${BASE_URL}/map.php`);
    await expect(page.locator('.warning-panel, .empty-state')).not.toContainText('Guest mode');
  });
});
