const puppeteer = require('puppeteer');

const APP_BASE = 'http://localhost:8080';

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function registerAndLogin(page) {
  await page.goto(`${APP_BASE}/register.php`, { waitUntil: 'networkidle0' });

  const email = `golby_extended_${Date.now()}@example.com`;
  await page.type('input[name="display_name"]', 'Golby Extended Tester');
  await page.type('input[name="email"]', email);
  await page.type('input[name="password"]', 'TestPass123!');

  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle0' }),
    page.click('button[type="submit"]'),
  ]);

  await page.goto(`${APP_BASE}/login.php`, { waitUntil: 'networkidle0' });
  await page.type('input[name="email"]', email);
  await page.type('input[name="password"]', 'TestPass123!');

  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle0' }),
    page.click('button[type="submit"]'),
  ]);

  return { email, password: 'TestPass123!' };
}

describe('Golby onboarding persistence and assistant integration', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({ headless: true });
    page = await browser.newPage();
  }, 30000);

  afterAll(async () => {
    await browser.close();
  });

  it('persists completion and keeps key authenticated pages quiet afterward', async () => {
    await registerAndLogin(page);
    await page.waitForSelector('#golby-onboarding-shell:not([hidden])', { timeout: 15000 });

    while (await page.$('[data-golby-onboarding-action="next"]')) {
      await page.click('[data-golby-onboarding-action="next"]');
      await sleep(150);
      if ((await page.$('#golby-onboarding-shell:not([hidden])')) === null) {
        break;
      }
    }

    for (const path of ['/index.php', '/profile.php', '/assistant.php']) {
      await page.goto(`${APP_BASE}${path}`, { waitUntil: 'networkidle0' });
      expect(await page.$('#golby-onboarding-shell')).toBeNull();
    }
  }, 120000);

  it('still leaves the assistant widget usable on the web shell', async () => {
    await page.goto(`${APP_BASE}/assistant.php`, { waitUntil: 'networkidle0' });
    await page.waitForSelector('button[aria-label="Get started with Golby"]', { timeout: 15000 });

    const welcomeLabel = await page.$eval('[aria-label="Welcome to Golby AI Assistant"]', (el) => el.getAttribute('aria-label') || '');
    expect(welcomeLabel).toBe('Welcome to Golby AI Assistant');

    const getStartedText = await page.$eval('button[aria-label="Get started with Golby"]', (el) => el.textContent || '');
    expect(getStartedText).toContain('Get Started');
  }, 120000);
});
