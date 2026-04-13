import React from 'react';
import { createRoot } from 'react-dom/client';
import '../public/assets/theme_tokens.css';
import '../public/assets/theme.css';
import '../public/assets/app.css';
import './golby-widget.css';
import { GolbyAssistantWidget } from '../components/golby/GolbyAssistantWidget';

function renderBootstrapError(message: string) {
  const mount = document.getElementById('riskradar-ai-assistant-widget');
  if (!mount) {
    return;
  }

  const existing = mount.querySelector('[data-golby-bootstrap-error]');
  if (existing) {
    return;
  }

  const box = document.createElement('div');
  box.setAttribute('data-golby-bootstrap-error', 'true');
  box.className = 'golby-bootstrap-error';
  box.textContent = message;
  mount.appendChild(box);
}

try {
  const mount = document.getElementById('riskradar-ai-assistant-widget');
  if (mount) {
    const root = createRoot(mount);
    root.render(<GolbyAssistantWidget />);
  }
} catch (error) {
  // Provide a visible fallback in case widget bootstrap fails at runtime.
  console.error('Golby bootstrap failed', error);
  renderBootstrapError('Golby is temporarily unavailable. Please refresh and try again.');
}
