const puppeteer = require('puppeteer');

describe('Golby Onboarding Tutorial', () => {
  let browser, page;
  beforeAll(async () => {
    browser = await puppeteer.launch({ headless: true });
    page = await browser.newPage();
  }, 30000); // 30 seconds
  afterAll(async () => {
    await browser.close();
  });

  it('shows onboarding for new user', async () => {
    await page.goto('http://localhost:8080/register.php');
    // Fill registration form with random email
    await page.type('input[name="display_name"]', 'Test User');
    const email = `testuser_${Date.now()}@example.com`;
    await page.type('input[name="email"]', email);
    await page.type('input[name="password"]', 'TestPass123!');
    await page.type('input[name="zip_code"]', '12345');
    console.log('DEBUG: Submitting registration form');
    await page.click('button[type="submit"]');
    // Wait for redirect to login, then login
    try {
      await page.waitForNavigation({ timeout: 60000, waitUntil: 'domcontentloaded' });
      console.log('DEBUG: Registration navigation completed');
    } catch (e) {
      console.log('DEBUG: Registration navigation TIMEOUT', e);
      throw e;
    }
    await page.type('input[name="email"]', email);
    await page.type('input[name="password"]', 'TestPass123!');
    await page.click('button[type="submit"]');
    try {
      await page.waitForNavigation({ timeout: 60000, waitUntil: 'networkidle0' });
      console.log('DEBUG: Login navigation completed');
    } catch (e) {
      console.log('DEBUG: Login navigation TIMEOUT', e);
      throw e;
    }
    // Check for onboarding popup
    await page.waitForSelector('.golby-onboarding-step', { timeout: 15000 });
    const onboardingVisible = await page.$('.golby-onboarding-step') !== null;
    expect(onboardingVisible).toBe(true);
  }, 120000);

  it('does not show onboarding for returning user', async () => {
    // Assume previous test created a user and completed onboarding
    // Log in again
    await page.goto('http://localhost:8080/login.php');
    // Use the same email and password
    await page.type('input[name="email"]', 'testuser@example.com');
    await page.type('input[name="password"]', 'TestPass123!');
    await page.click('button[type="submit"]');
    await page.waitForNavigation();
    // Confirm onboarding does not appear
    const onboardingVisible = await page.$('.golby-onboarding-step') !== null;
    expect(onboardingVisible).toBe(false);
  }, 30000);
});
