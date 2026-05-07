const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './frontend/web/tests/e2e',
  timeout: 90000,
  expect: { timeout: 10000 },
  fullyParallel: false,
  retries: 0,
  use: {
    headless: true,
    viewport: { width: 1366, height: 900 },
    ignoreHTTPSErrors: true,
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'static/evidence/playwright-report' }]]
});
