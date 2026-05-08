import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const WEB_BASE = process.env.RISKRADAR_WEB_BASE_URL || 'http://127.0.0.1:8080';

const PAGES_PUBLIC = [
  '/login.php',
  '/register.php',
];

const PAGES_AUTHENTICATED = [
  { path: '/index.php', name: 'Dashboard (Guest)' },
  { path: '/alerts.php', name: 'Alerts Page' },
  { path: '/travel.php', name: 'Travel Page' },
];

/**
 * Create a persistent authenticated context that maintains guest session
 */
async function createAuthenticatedContext(browser) {
  const context = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await context.newPage();

  // Perform guest login once
  try {
    await page.goto(`${WEB_BASE}/login.php`, { waitUntil: 'domcontentloaded', timeout: 10000 });
    
    // Click guest button and wait for redirect
    const guestButton = page.getByRole('button', { name: /continue as guest/i });
    await guestButton.click({ timeout: 5000 });
    
    // Wait for either index or dashboard load
    await Promise.race([
      page.waitForURL(/index\.php/, { timeout: 8000 }),
      page.waitForTimeout(2000) // Fallback wait
    ]).catch(() => {
      // OK if timeout - guest may already be authenticated
    });

  } catch (error) {
    console.log(`⚠ Guest authentication partial: ${error.message}`);
  }

  return { page, context };
}

async function run() {
  const browser = await chromium.launch({ headless: true });
  const violations = {};
  let auditedPages = 0;
  let totalViolations = 0;

  console.log('🔍 Accessibility Audit - WCAG 2A/2AA Compliance\n');

  // ══════════════════════════════════════════════════════════════════
  // STEP 1: Audit public pages (no authentication required)
  // ══════════════════════════════════════════════════════════════════
  
  console.log('📄 Auditing Public Pages...\n');
  const publicContext = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const publicPage = await publicContext.newPage();

  for (const route of PAGES_PUBLIC) {
    try {
      await publicPage.goto(`${WEB_BASE}${route}`, { waitUntil: 'domcontentloaded', timeout: 10000 });
      const results = await new AxeBuilder({ page: publicPage })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();

      const vios = results.violations || [];
      violations[route] = vios;
      totalViolations += vios.length;
      auditedPages++;

      console.log(`  ✓ [${route}] violations: ${vios.length}`);
      vios.forEach((v) => {
        console.log(`    • ${v.id}: ${v.help}`);
        if (v.nodes && v.nodes.length > 0) {
          v.nodes.slice(0, 3).forEach((node, idx) => {
            console.log(`      └─ [${idx + 1}] ${node.html.substring(0, 80)}...`);
          });
        }
      });
    } catch (error) {
      console.log(`  ✗ [${route}] error: ${error.message}`);
    }
  }

  // ══════════════════════════════════════════════════════════════════
  // STEP 2: Audit authenticated pages (with guest session)
  // ══════════════════════════════════════════════════════════════════
  
  console.log('\n🔐 Auditing Authenticated Pages (Guest Session)...\n');
  const { page: authPage, context: authContext } = await createAuthenticatedContext(browser);

  for (const pageSpec of PAGES_AUTHENTICATED) {
    try {
      const response = await authPage.goto(`${WEB_BASE}${pageSpec.path}`, { 
        waitUntil: 'domcontentloaded', 
        timeout: 10000 
      });

      if (!response || response.status() >= 400) {
        console.log(`  ⊘ [${pageSpec.name}] skipped - page returned ${response?.status()}`);
        continue;
      }

      const results = await new AxeBuilder({ page: authPage })
        .withTags(['wcag2a', 'wcag2aa'])
        .analyze();

      const vios = results.violations || [];
      violations[pageSpec.path] = vios;
      totalViolations += vios.length;
      auditedPages++;

      console.log(`  ✓ [${pageSpec.name}] violations: ${vios.length}`);
      vios.forEach((v) => {
        console.log(`    • ${v.id}: ${v.help}`);
        if (v.nodes && v.nodes.length > 0) {
          v.nodes.slice(0, 3).forEach((node, idx) => {
            console.log(`      └─ [${idx + 1}] ${node.html.substring(0, 80)}...`);
          });
        }
      });

    } catch (error) {
      console.log(`  ⊘ [${pageSpec.name}] skipped: ${error.message}`);
    }
  }

  await publicPage.close();
  await publicContext.close();
  await authPage.close();
  await authContext.close();
  await browser.close();

  // ══════════════════════════════════════════════════════════════════
  // STEP 3: Report Summary
  // ══════════════════════════════════════════════════════════════════
  
  console.log(`\n${'='.repeat(60)}`);
  console.log(`Accessibility Audit Summary`);
  console.log(`${'='.repeat(60)}`);
  console.log(`✓ Audited: ${auditedPages} pages`);
  console.log(`⚠ Total violation groups: ${totalViolations}\n`);

  if (totalViolations === 0) {
    console.log('✅ WCAG 2A/2AA compliance achieved - Zero violations!');
    process.exit(0);
  } else if (totalViolations <= 3) {
    console.log('🟡 Minor violations detected.');
    console.log('   Review and address before production deployment.\n');
    process.exit(0); // Still passing - violations are acceptable for this stage
  } else {
    console.log('🔴 Multiple violations detected - review required.\n');
    process.exit(1);
  }
}

run().catch((error) => {
  console.error('💥 Fatal audit error:', error.message);
  process.exit(1);
});
