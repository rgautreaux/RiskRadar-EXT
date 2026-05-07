import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';

const PAGES = [
  '/login.php',
  '/register.php',
  '/index.php',
  '/alerts.php',
  '/map.php',
  '/assistant.php',
  '/travel.php'
];

async function continueAsGuest(page) {
  await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
  await page.getByRole('button', { name: /continue as guest/i }).click();
  await page.waitForURL(/index\.php/);
}

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await context.newPage();

  await continueAsGuest(page);

  let totalViolations = 0;

  for (const route of PAGES) {
    await page.goto(`${WEB_BASE}${route}`, { waitUntil: 'domcontentloaded' });
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    const violations = results.violations || [];
    totalViolations += violations.length;

    console.log(`\\n[${route}] violations: ${violations.length}`);
    violations.forEach((v) => {
      console.log(`- ${v.id}: ${v.help}`);
    });
  }

  await browser.close();

  if (totalViolations > 0) {
    throw new Error(`Accessibility audit failed with ${totalViolations} violation groups.`);
  }

  console.log('Accessibility audit passed with zero violation groups.');
}

run().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
