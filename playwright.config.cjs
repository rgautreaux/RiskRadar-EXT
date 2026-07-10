/**
 * Playwright configuration for RiskRadar frontend E2E tests
 * Tests live in `frontend/web/tests/e2e` and expect the frontend to
 * be reachable at `http://127.0.0.1:8080` by default.
 */
module.exports = {
  testDir: './frontend/web/tests/e2e',
  timeout: 120000,
  expect: { timeout: 10000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: [['list'], ['html', { outputFolder: 'playwright-report' }]],
  use: {
    headless: true,
    baseURL: process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080',
    viewport: { width: 1280, height: 720 },
    actionTimeout: 0,
    trace: 'on-first-retry',
  },
};
