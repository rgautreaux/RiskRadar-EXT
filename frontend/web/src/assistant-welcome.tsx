import React from 'react';
import { createRoot } from 'react-dom/client';
import './golby-widget.css';
import { PageWelcome } from '../components/golby/PageWelcome';
import { PageChat } from '../components/golby/PageChat';

const ASSISTANT_WELCOME_SEEN_KEY = 'golby-assistant-welcome-seen';

declare global {
  interface Window {
    __RISKRADAR_ASSISTANT_ROOT__?: ReturnType<typeof createRoot>;
  }
}

function AssistantPageWrapper() {
  const [showWelcome, setShowWelcome] = React.useState(true);
  const [welcomeSeen, setWelcomeSeen] = React.useState(false);
  const [pageContext] = React.useState('assistant');

  React.useEffect(() => {
    try {
      const hasSeen = window.sessionStorage.getItem(ASSISTANT_WELCOME_SEEN_KEY) === 'true';
      setWelcomeSeen(hasSeen);
      setShowWelcome(!hasSeen);
    } catch {
      setShowWelcome(true);
      setWelcomeSeen(false);
    }
  }, []);

  const handleGetStarted = React.useCallback(() => {
    setShowWelcome(false);
    setWelcomeSeen(true);
    try {
      window.sessionStorage.setItem(ASSISTANT_WELCOME_SEEN_KEY, 'true');
    } catch {
      // Ignore storage failures
    }
  }, []);

  const handleBackToWelcome = React.useCallback(() => {
    setShowWelcome(true);
    try {
      window.sessionStorage.removeItem(ASSISTANT_WELCOME_SEEN_KEY);
    } catch {
      // Ignore storage failures
    }
  }, []);

  return (
    <>
      {showWelcome ? (
        <PageWelcome onGetStarted={handleGetStarted} />
      ) : (
        <PageChat
          pageContext={pageContext}
          onBack={handleBackToWelcome}
        />
      )}
    </>
  );
}

function renderAssistantPage() {
  const mount = document.getElementById('riskradar-assistant-page-welcome');
  if (mount) {
    window.__RISKRADAR_ASSISTANT_ROOT__ ??= createRoot(mount);
    window.__RISKRADAR_ASSISTANT_ROOT__.render(<AssistantPageWrapper />);
  }
}

try {
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', renderAssistantPage);
  } else {
    renderAssistantPage();
  }
} catch (error) {
  console.error('Assistant page wrapper failed', error);
}
