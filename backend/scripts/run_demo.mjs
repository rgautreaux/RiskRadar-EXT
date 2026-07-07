import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, '..', '..');
const demoDir = resolve(scriptDir, '..', 'demo');
const isWindows = process.platform === 'win32';

// Resolve Python interpreter from project venv
const pythonPath = isWindows
  ? resolve(repoRoot, '.venv', 'Scripts', 'python.exe')
  : resolve(repoRoot, '.venv', 'bin', 'python');

if (!existsSync(pythonPath)) {
  console.error(`❌ Unable to find project Python interpreter at: ${pythonPath}`);
  console.error('   Please ensure the project virtual environment is set up.');
  console.error('   Run: python -m venv .venv (from repository root)');
  process.exit(1);
}

// Determine which Python script to run and what arguments to pass
let pythonScript;
const args = [];

// Parse npm script arguments
const npmArgs = process.argv.slice(2);

// Handle different demo modes
if (npmArgs.includes('--clean')) {
  pythonScript = resolve(demoDir, 'seed_demo_data.py');
  args.push('--mode', 'reset');
  args.push('--clean-only');
} else if (npmArgs.includes('--verify')) {
  pythonScript = resolve(demoDir, 'seed_demo_data.py');
  args.push('--verify');
} else if (npmArgs.includes('--info')) {
  pythonScript = resolve(demoDir, 'seed_demo_data.py');
  args.push('--info');
} else if (npmArgs.includes('--generate-alerts')) {
  pythonScript = resolve(demoDir, 'mock_alert_generator.py');
  // Parse additional arguments
  const countIdx = npmArgs.indexOf('--count');
  if (countIdx !== -1 && countIdx + 1 < npmArgs.length) {
    args.push('--count', npmArgs[countIdx + 1]);
  }
  const typeIdx = npmArgs.indexOf('--type');
  if (typeIdx !== -1 && typeIdx + 1 < npmArgs.length) {
    args.push('--alert-type', npmArgs[typeIdx + 1]);
  }
} else {
  // Default to seed_demo_data.py with mode argument
  pythonScript = resolve(demoDir, 'seed_demo_data.py');
  
  // Extract mode from npm args (--mode fresh, --mode seed, --mode reset)
  const modeIdx = npmArgs.indexOf('--mode');
  if (modeIdx !== -1 && modeIdx + 1 < npmArgs.length) {
    args.push('--mode', npmArgs[modeIdx + 1]);
  } else {
    // Default to fresh
    args.push('--mode', 'fresh');
  }
}

if (!existsSync(pythonScript)) {
  console.error(`❌ Unable to find demo script at: ${pythonScript}`);
  process.exit(1);
}

// Spawn the Python script with inherited stdio for live output
const result = spawnSync(pythonPath, [pythonScript, ...args], {
  stdio: 'inherit',
  cwd: repoRoot,
  env: {
    ...process.env,
    PYTHONPATH: resolve(repoRoot, 'backend'),
  },
});

process.exit(result.status ?? 1);
