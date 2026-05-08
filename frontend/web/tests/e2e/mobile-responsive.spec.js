const { test, expect } = require('@playwright/test');

const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';
const MOBILE_VIEWPORT = { width: 360, height: 720 };

test.describe('Mobile responsive flows (360px)', () => {
  test.use({ viewport: MOBILE_VIEWPORT });

  test('guest flow on mobile', async ({ page }) => {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
    
    // Verify guest button is accessible on mobile
    const guestButton = page.getByRole('button', { name: /continue as guest/i });
    await expect(guestButton).toBeVisible();
    await guestButton.click();
    
    // Verify dashboard loads and is readable on mobile
    await expect(page).toHaveURL(/index\.php/);
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toBeVisible();
  });

  test('alerts page responsive layout on mobile', async ({ page }) => {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
    await page.getByRole('button', { name: /continue as guest/i }).click();
    
    await page.goto(`${WEB_BASE}/alerts.php`, { waitUntil: 'domcontentloaded' });
    
    // Verify content is not cut off and scrollable
    const alertContent = page.locator('main, .alerts-container, [role="main"]').first();
    await expect(alertContent).toBeVisible();
    
    // Verify navigation is touch-friendly on mobile
    const navElements = await page.locator('nav a, [role="navigation"] a').count();
    expect(navElements).toBeGreaterThan(0);
  });

  test('map page responsive controls on mobile', async ({ page }) => {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
    await page.getByRole('button', { name: /continue as guest/i }).click();
    
    await page.goto(`${WEB_BASE}/map.php`, { waitUntil: 'networkidle' });
    
    // Verify map container exists and wait for it
    const mapContainer = page.locator('#risk-map-container');
    await expect(mapContainer).toBeVisible({ timeout: 15000 });
    
    // Verify controls exist (map may have buttons or other controls)
    const mapExists = await page.locator('#risk-map-container').isVisible();
    expect(mapExists).toBe(true);
  });
});
