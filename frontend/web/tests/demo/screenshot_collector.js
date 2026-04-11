/* eslint-disable no-console */
const fs = require('node:fs');
const path = require('node:path');

class ScreenshotCollector {
  constructor(outputDir = './static/evidence/demo_screenshots') {
    this.outputDir = outputDir;
    this.screenshots = [];
    fs.mkdirSync(this.outputDir, { recursive: true });
  }

  async capture(page, name, description = '') {
    const safeName = name.replace(/[^a-zA-Z0-9_-]/g, '_');
    const filename = `demo_${safeName}.png`;
    const fullPath = path.resolve(this.outputDir, filename);

    await page.screenshot({ path: fullPath, fullPage: true });

    const record = {
      filename,
      path: fullPath,
      description,
      capturedAt: new Date().toISOString(),
      url: page.url(),
    };
    this.screenshots.push(record);
    console.log(`📷 Captured screenshot: ${filename}`);
    return record;
  }

  async saveManifest() {
    const manifestPath = path.resolve(this.outputDir, 'manifest.json');
    const payload = {
      generatedAt: new Date().toISOString(),
      count: this.screenshots.length,
      screenshots: this.screenshots,
    };
    fs.writeFileSync(manifestPath, `${JSON.stringify(payload, null, 2)}\n`, 'utf-8');
    console.log(`📋 Saved screenshot manifest: ${manifestPath}`);
    return manifestPath;
  }
}

module.exports = { ScreenshotCollector };
