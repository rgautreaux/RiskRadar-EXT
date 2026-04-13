import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const scriptDir = dirname(fileURLToPath(import.meta.url));
const repoRoot = resolve(scriptDir, '..', '..');
const isWindows = process.platform === 'win32';
const pythonPath = isWindows
  ? resolve(repoRoot, '.venv', 'Scripts', 'python.exe')
  : resolve(repoRoot, '.venv', 'bin', 'python');

if (!existsSync(pythonPath)) {
  console.error(`Unable to find project Python interpreter at: ${pythonPath}`);
  process.exit(1);
}

const result = spawnSync(
  pythonPath,
  [resolve(scriptDir, 'pre_demo_connectivity_check.py')],
  {
    stdio: 'inherit',
    cwd: repoRoot,
  },
);

process.exit(result.status ?? 1);
