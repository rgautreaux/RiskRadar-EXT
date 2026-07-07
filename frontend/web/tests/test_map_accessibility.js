// test_map_accessibility.js
// Automated accessibility and navigation tests for Risk Map using axe-core and basic DOM checks

const { AxePuppeteer } = require('axe-puppeteer');
const puppeteer = require('puppeteer');

const BASE_URL = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';

async function continueAsGuest(page) {
  await page.goto(`${BASE_URL}/login.php`, { waitUntil: 'networkidle2' });
  await page.waitForSelector('button[name="action"][value="guest"]', { timeout: 10000 });
  await page.click('button[name="action"][value="guest"]');
  await page.waitForNavigation({ waitUntil: 'networkidle2' });
}

describe('Risk Map Accessibility & Navigation', () => {
  let browser, page;
  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
    await continueAsGuest(page);
    await page.goto(`${BASE_URL}/map.php`, { waitUntil: 'networkidle2' });
  });
  afterAll(async () => {
    await browser.close();
  });

  it('should have no critical accessibility violations (axe)', async () => {
    const results = await new AxePuppeteer(page).analyze();
    expect(results.violations.length).toBe(0);
  });

  it('should allow Tab navigation to all controls and overlays', async () => {
    const tabOrder = [];
    await page.keyboard.press('Tab');
    for (let i = 0; i < 10; i++) {
      const active = await page.evaluate(() => document.activeElement.id);
      tabOrder.push(active);
      await page.keyboard.press('Tab');
    }
    expect(tabOrder).toContain('toggle-alerts');
    expect(tabOrder).toContain('region-filter');
    expect(tabOrder).toContain('risk-map-container');
  });

  it('should open marker modal with keyboard', async () => {
    await page.focus('#risk-map-container');
    await page.keyboard.press('Tab'); // Focus first marker
    await page.keyboard.press('Enter');
    const modalVisible = await page.evaluate(() => {
      const m = document.getElementById('marker-modal');
      return m && m.style.display === 'flex';
    });
    expect(modalVisible).toBe(true);
  });
});
