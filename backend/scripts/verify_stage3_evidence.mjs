import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, '..', '..');

const requiredArtifacts = [
  'static/evidence/s3-map-desktop-overlays.png',
  'static/evidence/s3-map-desktop-controls-legend.png',
  'static/evidence/s3-map-desktop-personalized.png',
  'static/evidence/s3-map-mobile-layout.png',
  'static/evidence/s3-map-mobile-controls.png',
  'static/evidence/s3-map-walkthrough.mp4',
  'static/evidence/s3-map-keyboard-nav.mp4',
];

const verificationDoc = resolve(
  repoRoot,
  'docs',
  'PLANNING_DOCS',
  'STAGE3_DOCS',
  'STAGE3_VERIFICATION_EVIDENCE.md'
);

let missing = 0;

console.log('== Stage 3 S3-06 evidence verification ==');
for (const relPath of requiredArtifacts) {
  const absPath = resolve(repoRoot, relPath);
  const ok = existsSync(absPath);
  console.log(`${ok ? 'OK  ' : 'MISS'} ${relPath}`);
  if (!ok) missing += 1;
}

if (!existsSync(verificationDoc)) {
  console.error('MISS docs/PLANNING_DOCS/STAGE3_DOCS/STAGE3_VERIFICATION_EVIDENCE.md');
  process.exit(1);
}

const verificationText = readFileSync(verificationDoc, 'utf8');
const linkMissing = requiredArtifacts.filter((relPath) => !verificationText.includes(relPath));

if (linkMissing.length > 0) {
  console.log('\nMissing links in STAGE3_VERIFICATION_EVIDENCE.md:');
  for (const relPath of linkMissing) {
    console.log(`- ${relPath}`);
  }
}

if (missing > 0 || linkMissing.length > 0) {
  console.error(
    `\nS3-06 closeout is incomplete: ${missing} artifact(s) missing, ${linkMissing.length} link(s) missing.`
  );
  process.exit(1);
}

console.log('\nPASS: S3-06 artifacts and links are complete.');
