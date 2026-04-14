// Minimal Playwright config to enable test discovery in frontend/web/tests
/** @type {import('@playwright/test').PlaywrightTestConfig} */
const config = {
  testDir: './frontend/web/tests',
  timeout: 60000,
  retries: 0,
  use: {
    headless: true,
    baseURL: 'http://localhost:8080',
  },
};

module.exports = config;
