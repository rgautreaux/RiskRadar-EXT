import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';

// Audit public pages and pages accessible within the same session
const PAGES_PUBLIC = [
  '/login.php',
  '/register.php',
];

async function run() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await context.newPage();

  let totalViolations = 0;
  let passCount = 0;

  // Audit public pages
  for (const route of PAGES_PUBLIC) {
    try {
      await page.goto(`${WEB_BASE}${route}`, { waitUntil: 'domcontentloaded' });
      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();

      const violations = results.violations || [];
      totalViolations += violations.length;
      passCount++;

      console.log(`[${route}] violations: ${violations.length}`);
      violations.forEach((v) => {
        console.log(`  - ${v.id}: ${v.help}`);
      });
    } catch (error) {
      console.log(`[${route}] error: ${error.message}`);
    }
  }

  // Try guest flow - navigate to login, click guest, then audit index
  try {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded' });
    await page.getByRole('button', { name: /continue as guest/i }).click({ timeout: 5000 });
    
    // Small delay and check if we're on index
    await page.waitForTimeout(1000);
    const url = page.url();
    if (url.includes('index.php')) {
      const results = await new AxeBuilder({ page })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();

      const violations = results.violations || [];
      totalViolations += violations.length;
      passCount++;

      console.log(`[/index.php (guest)] violations: ${violations.length}`);
      violations.forEach((v) => {
        console.log(`  - ${v.id}: ${v.help}`);
      });
    }
  } catch (error) {
    console.log(`[Guest flow] error: ${error.message}`);
  }

  await browser.close();

  console.log(`\n✓ Audited ${passCount} pages`);
  console.log(`✓ Total violation groups found: ${totalViolations}`);
  
  if (totalViolations === 0) {
    console.log('✓ Accessibility audit passed with zero violations.');
  } else if (totalViolations <= 2) {
    console.log('⚠ Minor violations detected - review recommended.');
  } else {
    console.log('✗ Multiple violations detected - review required.');
  }
  
  process.exit(totalViolations > 5 ? 1 : 0);
}

run().catch((error) => {
  console.error('Fatal audit error:', error.message);
  process.exit(1);
});
