/* eslint-disable no-console */
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const { ScreenshotCollector } = require('./screenshot_collector');

const REPO_ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const EVIDENCE_ROOT = path.resolve(REPO_ROOT, 'static', 'evidence');
const LOG_PATH = path.resolve(EVIDENCE_ROOT, 'demo_journey_log.json');

function parseArgs(argv) {
  const args = {
    baseUrl: 'http://localhost:8000',
    headless: true,
    pauseOnStep: false,
    screenshots: true,
    video: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === '--base-url' && argv[i + 1]) {
      args.baseUrl = argv[i + 1];
      i += 1;
    } else if (token === '--headless' && argv[i + 1]) {
      args.headless = argv[i + 1] !== 'false';
      i += 1;
    } else if (token === '--pause-on-step') {
      args.pauseOnStep = true;
    } else if (token === '--no-screenshots') {
      args.screenshots = false;
    } else if (token === '--video') {
      args.video = true;
    }
  }

  return args;
}

function ensureEvidenceDirs() {
  fs.mkdirSync(EVIDENCE_ROOT, { recursive: true });
  fs.mkdirSync(path.resolve(EVIDENCE_ROOT, 'demo_screenshots'), { recursive: true });
  fs.mkdirSync(path.resolve(EVIDENCE_ROOT, 'demo_videos'), { recursive: true });
}

async function waitForUi(page) {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(400);
}

async function pauseIfRequested(page, enabled, stepName) {
  if (!enabled) return;
  console.log(`\n⏸ Paused before: ${stepName}`);
  console.log('Press Enter in browser context prompt to continue...');
  await page.evaluate(() => {
    // eslint-disable-next-line no-alert
    alert('Demo paused. Click OK to continue.');
  });
}

async function stepNavigate(page, step, url, titleContains) {
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await waitForUi(page);
  const title = await page.title();
  if (titleContains && !title.toLowerCase().includes(titleContains.toLowerCase())) {
    console.warn(`⚠ Step ${step.id}: page title "${title}" did not include "${titleContains}"`);
  }
}

async function runJourney(options = {}) {
  ensureEvidenceDirs();
  const screenshotCollector = new ScreenshotCollector(path.resolve(EVIDENCE_ROOT, 'demo_screenshots'));

  const browser = await chromium.launch({ headless: options.headless });
  const context = await browser.newContext({
    viewport: { width: 1366, height: 900 },
    recordVideo: options.video
      ? {
          dir: path.resolve(EVIDENCE_ROOT, 'demo_videos'),
          size: { width: 1280, height: 720 },
        }
      : undefined,
  });

  const page = await context.newPage();
  const log = {
    startedAt: new Date().toISOString(),
    baseUrl: options.baseUrl,
    headless: options.headless,
    screenshots: options.screenshots,
    steps: [],
  };

  const recordStep = async (step, fn) => {
    const startedAt = Date.now();
    let status = 'passed';
    let error = null;
    try {
      await pauseIfRequested(page, options.pauseOnStep, step.name);
      await fn();
      if (options.screenshots) {
        await screenshotCollector.capture(page, `${String(step.id).padStart(2, '0')}_${step.slug}`, step.name);
      }
    } catch (err) {
      status = 'failed';
      error = String(err && err.message ? err.message : err);
      if (options.screenshots) {
        await screenshotCollector.capture(page, `${String(step.id).padStart(2, '0')}_${step.slug}_error`, `${step.name} (error)`);
      }
    }

    log.steps.push({
      id: step.id,
      slug: step.slug,
      name: step.name,
      status,
      durationMs: Date.now() - startedAt,
      error,
      url: page.url(),
      timestamp: new Date().toISOString(),
    });

    if (status === 'failed') {
      throw new Error(`Step ${step.id} failed: ${error}`);
    }
  };

  const base = options.baseUrl.replace(/\/$/, '');

  await recordStep(
    { id: 1, slug: 'dashboard', name: 'Dashboard Overview' },
    async () => {
      await stepNavigate(page, { id: 1 }, `${base}/index.php`, 'riskradar');
    },
  );

  await recordStep(
    { id: 2, slug: 'risk_scoring', name: 'Personalized Risk Scoring' },
    async () => {
      await stepNavigate(page, { id: 2 }, `${base}/risk.php?user_id=2&radius_km=50`, 'risk');
      await page.waitForSelector('h1:has-text("Personal risk score")', { timeout: 10000 });
    },
  );

  await recordStep(
    { id: 3, slug: 'smart_alerts', name: 'Smart Alerts Prioritization' },
    async () => {
      await stepNavigate(page, { id: 3 }, `${base}/smart_alerts.php?user_id=2&radius_km=100&limit=10`, 'smart');
      await page.waitForSelector('text=Prioritized alerts', { timeout: 10000 });
    },
  );

  await recordStep(
    { id: 4, slug: 'map', name: 'Interactive Risk Map' },
    async () => {
      await stepNavigate(page, { id: 4 }, `${base}/map.php`, 'map');
      await page.waitForTimeout(1500);
      const personalizedToggle = page.locator('#toggle-personalized');
      if (await personalizedToggle.count()) {
        await personalizedToggle.check({ force: true });
      }
    },
  );

  await recordStep(
    { id: 5, slug: 'forecast', name: 'Forecast View' },
    async () => {
      await stepNavigate(page, { id: 5 }, `${base}/forecast.php`, 'forecast');
      await page.waitForSelector('text=24–48 Hour Risk Forecast', { timeout: 10000 }).catch(() => {});
    },
  );

  await recordStep(
    { id: 6, slug: 'assistant', name: 'AI Assistant View' },
    async () => {
      await stepNavigate(page, { id: 6 }, `${base}/assistant.php`, 'assistant');

      const openWidgetButton = page.getByRole('button', { name: 'Open Golby AI Assistant' });
      await openWidgetButton.waitFor({ timeout: 10000 });
      await openWidgetButton.click();

      const messageInput = page.getByRole('textbox', { name: 'Message input' });
      await messageInput.waitFor({ timeout: 10000 });

      const helpfulFeedbackButtons = page.getByRole('button', { name: 'This was helpful' });
      const helpfulCountBefore = await helpfulFeedbackButtons.count();

      await messageInput.fill('Show me latest alerts');
      await page.getByRole('button', { name: 'Send message' }).click();
      await page.waitForFunction(
        () => {
          const buttons = Array.from(document.querySelectorAll('button[aria-label="This was helpful"]'));
          return buttons.length >= 2;
        },
        null,
        { timeout: 15000 },
      );

      const helpfulCountAfter = await helpfulFeedbackButtons.count();
      if (helpfulCountAfter <= helpfulCountBefore) {
        throw new Error('Expected a new assistant response with feedback controls.');
      }

      if (options.screenshots) {
        await screenshotCollector.capture(page, '06a_assistant_response', 'Assistant reply rendered after sending a prompt');
      }

      await helpfulFeedbackButtons.first().click();
      if (options.screenshots) {
        await screenshotCollector.capture(page, '06b_assistant_feedback', 'Assistant feedback interaction complete');
      }

      await messageInput.fill('Can you give me medical advice?');
      await page.getByRole('button', { name: 'Send message' }).click();
      await page.waitForSelector('text=I cannot provide medical advice', { timeout: 15000 });

      if (options.screenshots) {
        await screenshotCollector.capture(page, '06c_assistant_guardrail', 'Assistant guardrail response rendered');
      }
    },
  );

  await screenshotCollector.saveManifest();
  log.screenshots = screenshotCollector.screenshots;
  log.finishedAt = new Date().toISOString();
  log.overallStatus = 'passed';

  fs.writeFileSync(LOG_PATH, `${JSON.stringify(log, null, 2)}\n`, 'utf-8');

  await context.close();
  await browser.close();

  return log;
}

async function main() {
  const options = parseArgs(process.argv.slice(2));
  console.log('📊 Running RiskRadar demo journey...');
  console.log(`Base URL: ${options.baseUrl}`);
  const result = await runJourney(options);
  const passed = result.steps.filter((s) => s.status === 'passed').length;
  console.log(`✅ Journey complete: ${passed}/${result.steps.length} steps passed`);
  console.log(`📁 Log written: ${LOG_PATH}`);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(`❌ Demo journey failed: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { runJourney, parseArgs };
