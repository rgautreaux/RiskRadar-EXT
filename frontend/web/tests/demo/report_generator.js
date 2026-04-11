/* eslint-disable no-console */
const fs = require('node:fs');
const path = require('node:path');

const REPO_ROOT = path.resolve(__dirname, '..', '..', '..', '..');
const EVIDENCE_ROOT = path.resolve(REPO_ROOT, 'static', 'evidence');
const LOG_PATH = path.resolve(EVIDENCE_ROOT, 'demo_journey_log.json');
const SCREENSHOT_MANIFEST = path.resolve(EVIDENCE_ROOT, 'demo_screenshots', 'manifest.json');
const DEFAULT_OUTPUT = path.resolve(EVIDENCE_ROOT, 'DEMO_REPORT.md');

function readJsonSafe(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch {
    return fallback;
  }
}

class ReportGenerator {
  constructor(demoLog = {}, screenshotManifest = {}) {
    this.demoLog = demoLog;
    this.screenshotManifest = screenshotManifest;
    this.report = '';
  }

  async generate() {
    const steps = Array.isArray(this.demoLog.steps) ? this.demoLog.steps : [];
    const screenshots = Array.isArray(this.screenshotManifest.screenshots)
      ? this.screenshotManifest.screenshots
      : [];

    const stepRows = steps
      .map(
        (s) => `| ${s.id} | ${s.name} | ${s.status} | ${s.durationMs} | ${s.url || ''} | ${s.error || ''} |`,
      )
      .join('\n');

    const screenshotRows = screenshots
      .map((s) => {
        const rel = path.relative(REPO_ROOT, s.path).replace(/\\/g, '/');
        return `- ${s.filename}: ${s.description || 'Screenshot'} (${rel})`;
      })
      .join('\n');

    this.report = `# Demo Evidence Report\n\n` +
      `Generated: ${new Date().toISOString()}\n\n` +
      `## Run Summary\n\n` +
      `- Base URL: ${this.demoLog.baseUrl || 'unknown'}\n` +
      `- Started: ${this.demoLog.startedAt || 'unknown'}\n` +
      `- Finished: ${this.demoLog.finishedAt || 'unknown'}\n` +
      `- Overall Status: ${this.demoLog.overallStatus || 'unknown'}\n` +
      `- Steps Executed: ${steps.length}\n\n` +
      `## Step Results\n\n` +
      `| Step | Name | Status | Duration (ms) | URL | Error |\n` +
      `|---|---|---|---:|---|---|\n` +
      `${stepRows || '| - | No steps recorded | - | - | - | - |'}\n\n` +
      `## Captured Screenshots\n\n` +
      `${screenshotRows || '- No screenshots were captured.'}\n\n` +
      `## Stage Coverage\n\n` +
      `- Stage 1: Dashboard and baseline web navigation\n` +
      `- Stage 2: Risk scoring and prioritized alerts\n` +
      `- Stage 3: Interactive map load and personalization toggle\n` +
      `- Stage 4: Forecast and assistant page flows\n\n` +
      `## Notes\n\n` +
      `Use this report with docs/DEMO_RUNBOOK.md and docs/DEMO_FEATURES_BY_STAGE.md for grading evidence.\n`;

    return { status: 'report_generated', format: 'markdown', contentLength: this.report.length };
  }

  async save(outputPath = DEFAULT_OUTPUT) {
    const outDir = path.dirname(outputPath);
    fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(outputPath, this.report, 'utf-8');
    console.log(`💾 Report saved: ${outputPath}`);
    return outputPath;
  }
}

async function main() {
  const demoLog = readJsonSafe(LOG_PATH, {});
  const screenshotManifest = readJsonSafe(SCREENSHOT_MANIFEST, {});
  const generator = new ReportGenerator(demoLog, screenshotManifest);
  await generator.generate();
  await generator.save(DEFAULT_OUTPUT);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(`❌ Failed to generate report: ${err.message}`);
    process.exit(1);
  });
}

module.exports = { ReportGenerator };
