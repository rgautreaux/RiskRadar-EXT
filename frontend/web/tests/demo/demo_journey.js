/* eslint-disable no-console */
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const { chromium } = require('playwright');
const { ScreenshotCollector } = require('./screenshot_collector');

const REPO_ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const EVIDENCE_ROOT = path.resolve(REPO_ROOT, 'static', 'evidence');
const LOG_PATH = path.resolve(EVIDENCE_ROOT, 'demo_journey_log.json');
const SEED_METADATA_PATH = path.resolve(REPO_ROOT, 'seed_metadata.json');
const BACKEND_SEED_METADATA_PATH = path.resolve(REPO_ROOT, 'backend', 'seed_metadata.json');
const DEMO_FIXTURES_PATH = path.resolve(REPO_ROOT, 'backend', 'demo', 'fixtures.json');
const SESSION_COOKIE_NAME = 'riskradar_session';
const DEFAULT_JWT_SECRET = 'CHANGE-ME-set-a-real-secret-in-dotenv';
const SESSION_TTL_MINUTES = Number(process.env.ACCESS_TOKEN_EXPIRE_MINUTES || 60);

function parseArgs(argv) {
  const args = {
    baseUrl: 'http://127.0.0.1:8080',
    apiBaseUrl: 'http://127.0.0.1:8001',
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
    } else if (token === '--api-base-url' && argv[i + 1]) {
      args.apiBaseUrl = argv[i + 1];
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

async function continueAsGuest(page, baseUrl) {
  await page.goto(`${baseUrl}/login.php`, { waitUntil: 'domcontentloaded' });
  await waitForUi(page);

  const guestButton = page.locator('button[name="action"][value="guest"]');
  await guestButton.waitFor({ timeout: 10000 });
  await guestButton.click();
  await page.waitForURL('**/index.php', { timeout: 10000 });
  await waitForUi(page);
}

function readSeedMetadata() {
  const candidatePaths = [SEED_METADATA_PATH, BACKEND_SEED_METADATA_PATH];

  for (const metadataPath of candidatePaths) {
    if (!fs.existsSync(metadataPath)) {
      continue;
    }

    try {
      const raw = fs.readFileSync(metadataPath, 'utf-8');
      return JSON.parse(raw);
    } catch {
      // Try the next candidate metadata path.
    }
  }

  return null;
}

function getSessionTokenForUser(userId) {
  const metadata = readSeedMetadata();
  return metadata?.session_tokens?.[String(userId)]?.token ?? null;
}

function readDemoCredentials() {
  if (!fs.existsSync(DEMO_FIXTURES_PATH)) {
    return {};
  }

  try {
    const raw = fs.readFileSync(DEMO_FIXTURES_PATH, 'utf-8');
    const parsed = JSON.parse(raw);
    const users = Array.isArray(parsed?.users) ? parsed.users : [];
    return users.reduce((acc, user) => {
      const id = Number(user?.id);
      if (!Number.isFinite(id)) {
        return acc;
      }
      const email = user?.email_plaintext;
      const password = user?.password_plaintext;
      if (typeof email === 'string' && typeof password === 'string') {
        acc[id] = { email, password };
      }
      return acc;
    }, {});
  } catch {
    return {};
  }
}

async function clearSessionCookie(context) {
  await context.clearCookies();
}

async function _setCookieValue(context, baseUrl, token) {
  const target = new URL(baseUrl);
  await context.addCookies([
    {
      name: SESSION_COOKIE_NAME,
      value: token,
      domain: target.hostname,
      path: '/',
      httpOnly: true,
      secure: target.protocol === 'https:',
      sameSite: 'Lax',
    },
  ]);
}

async function _authMeOk(context, apiBaseUrl) {
  const authMeRes = await context.request.get(`${apiBaseUrl.replace(/\/$/, '')}/api/v1/auth/me`);
  return authMeRes.ok();
}

async function _loginAndSetCookie(context, baseUrl, apiBaseUrl, userId) {
  const credentialsByUserId = readDemoCredentials();
  const credentials = credentialsByUserId[userId];
  if (!credentials) {
    throw new Error(`Missing fixture credentials for user ${userId}.`);
  }

  const loginRes = await context.request.post(`${apiBaseUrl.replace(/\/$/, '')}/api/v1/auth/login`, {
    data: {
      email: credentials.email,
      password: credentials.password,
    },
  });

  if (!loginRes.ok()) {
    throw new Error(`Unable to login seeded user ${userId}; auth/login returned HTTP ${loginRes.status()}.`);
  }

  const loginJson = await loginRes.json();
  const token = loginJson?.session_token;
  if (typeof token !== 'string' || token.length < 10) {
    throw new Error(`auth/login returned an invalid session token for user ${userId}.`);
  }

  await _setCookieValue(context, baseUrl, token);
}

function _base64urlEncode(buffer) {
  return Buffer.from(buffer)
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/g, '');
}

function _resolveSessionSecret() {
  const keyMaterial =
    (process.env.JWT_SECRET_KEY || process.env.EMAIL_HASH_SECRET || process.env.EMAIL_ENCRYPTION_KEY || DEFAULT_JWT_SECRET).trim();
  return crypto.createHash('sha256').update(keyMaterial, 'utf8').digest();
}

function _createSessionTokenForUser(userId) {
  const nowEpoch = Math.floor(Date.now() / 1000);
  const expiresAtEpoch = nowEpoch + Math.max(1, SESSION_TTL_MINUTES) * 60;
  const payloadJson = JSON.stringify({ exp: expiresAtEpoch, iat: nowEpoch, sub: Number(userId) });
  const payloadPart = _base64urlEncode(Buffer.from(payloadJson, 'utf8'));
  const signature = crypto.createHmac('sha256', _resolveSessionSecret()).update(payloadPart, 'utf8').digest();
  return `${payloadPart}.${_base64urlEncode(signature)}`;
}

async function setSessionCookie(context, baseUrl, apiBaseUrl, userId) {
  const token = getSessionTokenForUser(userId);
  if (token) {
    await _setCookieValue(context, baseUrl, token);
    if (await _authMeOk(context, apiBaseUrl)) {
      return;
    }
    await clearSessionCookie(context);
  }

  try {
    await _loginAndSetCookie(context, baseUrl, apiBaseUrl, userId);
    if (await _authMeOk(context, apiBaseUrl)) {
      return;
    }
    await clearSessionCookie(context);
  } catch {
    await clearSessionCookie(context);
  }

  const generatedToken = _createSessionTokenForUser(userId);
  await _setCookieValue(context, baseUrl, generatedToken);
  if (!(await _authMeOk(context, apiBaseUrl))) {
    throw new Error(`Unable to establish authenticated session for user ${userId}.`);
  }
}

async function assertApiResponse(response, label, expectedStatus) {
  if (typeof expectedStatus === 'number') {
    if (response.status() !== expectedStatus) {
      throw new Error(`${label} expected HTTP ${expectedStatus} but received ${response.status()}`);
    }
    return;
  }

  if (!response.ok()) {
    throw new Error(`${label} failed with HTTP ${response.status()}`);
  }
}

async function assertAssistantContracts(page, baseUrl, role, userId) {
  const apiRoot = (baseUrl || '').replace(/\/$/, '');
  const apiBase = `${apiRoot}/api/v1`;
  const syntheticSession = `demo-${role}-${Date.now()}`;
  const syntheticMessage = `msg-${Date.now()}`;

  const alertsRes = await page.request.get(`${apiBase}/alerts?limit=2`);
  await assertApiResponse(alertsRes, `${role} alerts contract`);

  const riskMapRes = await page.request.get(`${apiBase}/risk/map`);
  await assertApiResponse(riskMapRes, `${role} risk map contract`);

  const forecastRes = await page.request.get(`${apiBase}/forecast?location=Baton%20Rouge`);
  await assertApiResponse(forecastRes, `${role} forecast contract`);

  const assistantRes = await page.request.post(`${apiBase}/assistant/respond`, {
    data: {
      message: 'Show me latest alerts',
      page_context: 'assistant',
      user_id: userId,
      location: 'Baton Rouge',
    },
  });
  await assertApiResponse(assistantRes, `${role} assistant contract`);
  const assistantJson = await assistantRes.json();
  if (!assistantJson || typeof assistantJson.reply !== 'string' || assistantJson.reply.length < 1) {
    throw new Error(`${role} assistant contract returned an invalid reply payload.`);
  }

  const authMeRes = await page.request.get(`${apiBase}/auth/me`);
  if (role === 'anonymous') {
    await assertApiResponse(authMeRes, `${role} auth/me contract`, 401);
  } else {
    await assertApiResponse(authMeRes, `${role} auth/me contract`);
  }

  const feedbackRes = await page.request.post(`${apiBase}/feedback`, {
    data: {
      session_id: syntheticSession,
      message_id: syntheticMessage,
      reaction: 'thumbs_up',
      rating: 5,
      page_context: 'assistant',
      response_category: 'live',
      response_text: 'Contract verification message',
      comment: `contract-${role}`,
    },
  });
  await assertApiResponse(feedbackRes, `${role} feedback contract`);

  const preferencesRes = await page.request.put(`${apiBase}/users/${userId}/preferences`, {
    data: {
      assistant_style_profile: {
        tone: {
          warmth: 0.6,
          calmness: 0.8,
          humor: 0.3,
        },
        delivery: {
          conciseness: 0.7,
          detail: 0.4,
          expandability: 0.5,
        },
        voice: {
          formality: 0.4,
        },
        learning: {
          feedback_count: 1,
          last_feedback_at: new Date().toISOString(),
        },
      },
    },
  });
  await assertApiResponse(preferencesRes, `${role} user preference sync contract`);
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
  const apiBase = (options.apiBaseUrl || options.baseUrl).replace(/\/$/, '');

  await recordStep(
    { id: 1, slug: 'login_gate_and_guest_entry', name: 'Login Gate and Guest Entry' },
    async () => {
      await page.goto(`${base}/index.php`, { waitUntil: 'domcontentloaded' });
      await waitForUi(page);
      if (!page.url().includes('/login.php')) {
        throw new Error(`Expected /index.php to redirect to /login.php, received ${page.url()}`);
      }

      await continueAsGuest(page, base);
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
      await clearSessionCookie(context);
      await assertAssistantContracts(page, apiBase, 'anonymous', 2);

      await clearSessionCookie(context);
      await setSessionCookie(context, base, apiBase, 2);
      await stepNavigate(page, { id: 6 }, `${base}/assistant.php`, 'assistant');
      await assertAssistantContracts(page, apiBase, 'user', 2);

      const widget = page.locator('#riskradar-ai-assistant-widget');
      const openWidgetButton = widget.getByRole('button', { name: 'Open Golby AI Assistant' });

      await openWidgetButton.waitFor({ timeout: 10000 });
      await openWidgetButton.click();

      const getStartedButton = widget.getByRole('button', { name: 'Get started with Golby' }).first();
      if (await getStartedButton.count()) {
        await getStartedButton.click({ force: true });
      }

      const messageInput = widget.getByRole('textbox', { name: 'Message input' });
      await messageInput.waitFor({ timeout: 10000 });

      const helpfulFeedbackButtons = widget.getByRole('button', { name: 'This was helpful' });
      const helpfulCountBefore = await helpfulFeedbackButtons.count();

      await messageInput.fill('Show me latest alerts');
      await widget.getByRole('button', { name: 'Send message' }).click({ force: true });
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
        await screenshotCollector.capture(page, '06b_assistant_response', 'Assistant reply rendered after sending a prompt');
      }

      await helpfulFeedbackButtons.first().click();
      if (options.screenshots) {
        await screenshotCollector.capture(page, '06c_assistant_feedback', 'Assistant feedback interaction complete');
      }

      await messageInput.fill('Can you give me medical advice?');
      await widget.getByRole('button', { name: 'Send message' }).click({ force: true });
      await page.waitForSelector('text=I cannot provide medical advice', { timeout: 15000 });

      if (options.screenshots) {
        await screenshotCollector.capture(page, '06d_assistant_guardrail', 'Assistant guardrail response rendered');
      }

      if (await widget.getByRole('button', { name: 'Show Panels' }).count()) {
        throw new Error('Authenticated non-admin users should not see diagnostics panel controls.');
      }

      await clearSessionCookie(context);
      await setSessionCookie(context, base, apiBase, 4);
      await stepNavigate(page, { id: 6 }, `${base}/assistant.php`, 'assistant');
      await assertAssistantContracts(page, apiBase, 'admin', 4);

      await openWidgetButton.waitFor({ timeout: 10000 });
      await openWidgetButton.click();

      const diagnosticsToggle = widget.getByRole('button', { name: 'Toggle diagnostics panel' });
      await diagnosticsToggle.waitFor({ timeout: 20000 });
      await diagnosticsToggle.click();

      if (options.screenshots) {
        await screenshotCollector.capture(page, '06e_assistant_admin_diagnostics', 'Admin diagnostics panel visibility check');
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
