// test_map_accessibility.js
// Automated accessibility and navigation tests for Risk Map using axe-core and basic DOM checks

const { AxePuppeteer } = require('axe-puppeteer');
const puppeteer = require('puppeteer');

describe('Risk Map Accessibility & Navigation', () => {
  let browser, page;
  beforeAll(async () => {
    browser = await puppeteer.launch();
    page = await browser.newPage();
    await page.goto('http://localhost:8000/web/views/map.php'); // Adjust URL as needed
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
