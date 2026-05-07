const puppeteer = require('puppeteer');

const APP_BASE = 'http://localhost:8080';
const AUTHENTICATED_PAGES = [
  '/index.php',
  '/alerts.php',
  '/summaries.php',
  '/profile.php',
  '/map.php',
  '/forecast.php',
  '/assistant.php',
];

async function registerUser(page) {
  await page.goto(`${APP_BASE}/register.php`, { waitUntil: 'networkidle0' });

  const email = `golby_${Date.now()}@example.com`;
  await page.type('input[name="display_name"]', 'Golby Tester');
  await page.type('input[name="email"]', email);
  await page.type('input[name="password"]', 'TestPass123!');
  await page.type('input[name="zip_code"]', '90210');

  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle0' }),
    page.click('button[type="submit"]'),
  ]);

  return { email, password: 'TestPass123!' };
}

async function loginUser(page, credentials) {
  await page.goto(`${APP_BASE}/login.php`, { waitUntil: 'networkidle0' });
  await page.type('input[name="email"]', credentials.email);
  await page.type('input[name="password"]', credentials.password);

  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle0' }),
    page.click('button[type="submit"]'),
  ]);
}

async function expectOnboardingVisible(page) {
  await page.waitForSelector('#golby-onboarding-shell:not([hidden])', { timeout: 15000 });
  const visible = await page.$('#golby-onboarding-shell:not([hidden])');
  expect(visible).not.toBeNull();
}

async function expectOnboardingHidden(page) {
  const visible = await page.$('#golby-onboarding-shell:not([hidden])');
  expect(visible).toBeNull();
}

async function expectWidgetHidden(page) {
  const mount = await page.$('#riskradar-ai-assistant-widget');
  expect(mount).toBeNull();
}

describe('Golby onboarding tutorial', () => {
  let browser;
  let page;

  beforeAll(async () => {
    browser = await puppeteer.launch({ headless: true });
    page = await browser.newPage();
  }, 30000);

  afterAll(async () => {
    await browser.close();
  });

  it('stays hidden on login and register pages before sign-in', async () => {
    await page.goto(`${APP_BASE}/login.php`, { waitUntil: 'networkidle0' });
    await expectOnboardingHidden(page);
    await expectWidgetHidden(page);

    await page.goto(`${APP_BASE}/register.php`, { waitUntil: 'networkidle0' });
    await expectOnboardingHidden(page);
    await expectWidgetHidden(page);
  }, 60000);

  it('appears on authenticated pages until the user finishes the tour', async () => {
    const credentials = await registerUser(page);
    await loginUser(page, credentials);

    for (const path of AUTHENTICATED_PAGES) {
      await page.goto(`${APP_BASE}${path}`, { waitUntil: 'networkidle0' });
      await expectOnboardingVisible(page);
      await page.screenshot({ path: `golby-onboarding-${path.replace(/\//g, '').replace('.php', '')}.png`, fullPage: true });
    }

    const nextButton = '[data-golby-onboarding-action="next"]';
    for (let step = 0; step < 3; step += 1) {
      await page.click(nextButton);
      await page.waitForFunction(
        (expectedStep) => document.querySelector('[data-golby-onboarding-counter]')?.textContent === expectedStep,
        {},
        `Step ${step + 2} of 4`,
      );
    }

    await Promise.all([
      page.waitForFunction(() => document.querySelector('#golby-onboarding-shell')?.hidden === true, { timeout: 10000 }),
      page.click(nextButton),
    ]);

    const onboardingHidden = await page.$('#golby-onboarding-shell:not([hidden])');
    expect(onboardingHidden).toBeNull();

    await page.goto(`${APP_BASE}/index.php`, { waitUntil: 'networkidle0' });
    await expectOnboardingHidden(page);

    await page.goto(`${APP_BASE}/alerts.php`, { waitUntil: 'networkidle0' });
    await expectOnboardingHidden(page);
  }, 120000);
});
