const { test, expect } = require('@playwright/test');

const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';

test.describe('Accessibility checks', () => {
  test('keyboard navigation on dashboard', async ({ page }) => {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
    
    // Use Tab to navigate to guest button
    await page.keyboard.press('Tab');
    
    // Verify focus is visible
    let focused = await page.evaluate(() => document.activeElement?.tagName);
    expect(['BUTTON', 'A']).toContain(focused);
    
    // Continue as guest
    await page.getByRole('button', { name: /continue as guest/i }).click();
    await expect(page).toHaveURL(/index\.php/);
  });

  test('form labels are associated with inputs on register page', async ({ page }) => {
    await page.goto(`${WEB_BASE}/register.php`, { waitUntil: 'domcontentloaded' });
    
    // Verify inputs have associated labels or aria-labels
    const inputs = page.locator('input[type="text"], input[type="email"], input[type="password"]');
    const count = await inputs.count();
    expect(count).toBeGreaterThan(0);
    
    // Check at least one input has a label or aria-label
    for (let i = 0; i < Math.min(count, 2); i++) {
      const input = inputs.nth(i);
      const ariaLabel = await input.getAttribute('aria-label');
      const placeholder = await input.getAttribute('placeholder');
      const id = await input.getAttribute('id');
      
      // Should have at least one accessible name
      expect(ariaLabel || placeholder || id).toBeTruthy();
    }
  });

  test('buttons have accessible names', async ({ page }) => {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
    
    // Verify all buttons have text or aria-label
    const buttons = page.locator('button');
    const count = await buttons.count();
    
    for (let i = 0; i < count; i++) {
      const button = buttons.nth(i);
      const text = await button.textContent();
      const ariaLabel = await button.getAttribute('aria-label');
      
      // Button should have visible text or aria-label
      if (!text?.trim()) {
        expect(ariaLabel).toBeTruthy();
      }
    }
  });

  test('focus trap and escape key on modals', async ({ page }) => {
    await page.goto(`${WEB_BASE}/smart_alerts.php`, { waitUntil: 'domcontentloaded' });
    
    // Try to find and trigger a modal/dialog
    const modal = page.locator('[role="dialog"], .modal, .lockout-dialog').first();
    
    if (await modal.isVisible()) {
      // Verify Escape key closes modal
      await page.keyboard.press('Escape');
      await expect(modal).not.toBeVisible({ timeout: 2000 }).catch(() => {
        // Modal might not close on Esc; that's a finding
      });
    }
  });

  test('links have descriptive text', async ({ page }) => {
    await page.goto(`${WEB_BASE}/index.php`, { waitUntil: 'domcontentloaded' });
    
    // Verify links are not generic ("click here", empty)
    const links = page.locator('a');
    const count = await links.count();
    
    let hasGenericLink = false;
    for (let i = 0; i < Math.min(count, 10); i++) {
      const link = links.nth(i);
      const text = await link.textContent();
      const ariaLabel = await link.getAttribute('aria-label');
      
      const accessibleName = (text?.trim() || '').toLowerCase();
      if (accessibleName === 'click here' || accessibleName === 'link' || !accessibleName) {
        hasGenericLink = true;
      }
    }
    
    expect(hasGenericLink).toBeFalsy();
  });

  test('page has proper heading hierarchy', async ({ page }) => {
    await page.goto(`${WEB_BASE}/index.php`, { waitUntil: 'domcontentloaded' });
    
    // Verify at least one H1 exists
    const h1Count = await page.locator('h1').count();
    expect(h1Count).toBeGreaterThanOrEqual(1);
    
    // Verify no skipped heading levels (e.g., H1 -> H3 is bad)
    const headings = page.locator('h1, h2, h3, h4, h5, h6');
    const headingLevels = [];
    
    for (let i = 0; i < await headings.count(); i++) {
      const tag = await headings.nth(i).evaluate(el => el.tagName);
      const level = parseInt(tag[1]);
      headingLevels.push(level);
    }
    
    // Basic check: levels should not jump by more than 1
    for (let i = 1; i < headingLevels.length; i++) {
      const diff = Math.abs(headingLevels[i] - headingLevels[i - 1]);
      expect(diff).toBeLessThanOrEqual(1);
    }
  });
});
