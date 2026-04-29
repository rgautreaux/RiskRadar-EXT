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
      await page.waitForSelector('.message-success', { timeout: 15000 });
      console.log('DEBUG: Registration success message detected');
    } catch (e) {
      console.log('DEBUG: Registration success message TIMEOUT', e);
      const content = await page.content();
      console.log('DEBUG: Registration page content after submit:', content);
      throw e;
    }
    await page.type('input[name="email"]', email);
    await page.type('input[name="password"]', 'TestPass123!');
    await page.click('button[type="submit"]');
    // Wait for onboarding popup after login
    try {
      await page.waitForSelector('.golby-onboarding-step', { timeout: 20000 });
      console.log('DEBUG: Onboarding popup detected after login');
    } catch (e) {
      console.log('DEBUG: Onboarding popup TIMEOUT after login', e);
      const content = await page.content();
      console.log('DEBUG: Page content after login:', content);
      await page.screenshot({ path: 'onboarding_after_login.png', fullPage: true });
      throw e;
    }
    const onboardingVisible = await page.$('.golby-onboarding-step') !== null;
    expect(onboardingVisible).toBe(true);
  }, 120000);

  it('does not show onboarding for returning user', async () => {
    // Log out if already logged in
    await page.goto('http://localhost:8080/logout.php');
    await page.goto('http://localhost:8080/login.php');
    // Use the same email and password
    await page.type('input[name="email"]', 'testuser@example.com');
    await page.type('input[name="password"]', 'TestPass123!');
    await page.click('button[type="submit"]');
    // Wait for possible onboarding popup
    try {
      await page.waitForTimeout(3000); // Give time for UI to update
    } catch (e) {}
    const onboardingVisible = await page.$('.golby-onboarding-step') !== null;
    expect(onboardingVisible).toBe(false);
  }, 120000);
});
