import React from 'react';
import { createRoot } from 'react-dom/client';
import './golby-widget.css';
import { PageWelcome } from '../components/golby/PageWelcome';
import { FloatingWidget } from '../components/golby/FloatingWidget';
import { ChatInterface } from '../components/golby/ChatInterface';
import { fetchCurrentUser } from '../components/golby/apiClient';

const ASSISTANT_WELCOME_SEEN_KEY = 'golby-assistant-welcome-seen';

function AssistantPageWrapper() {
  const [showWelcome, setShowWelcome] = React.useState(true);
  const [welcomeSeen, setWelcomeSeen] = React.useState(false);
  const [chatOpen, setChatOpen] = React.useState(false);
  const [pageContext] = React.useState('assistant');
  const [currentUserId, setCurrentUserId] = React.useState<number | undefined>(undefined);
  const [isAdmin, setIsAdmin] = React.useState(false);

  React.useEffect(() => {
    try {
      const hasSeen = window.sessionStorage.getItem(ASSISTANT_WELCOME_SEEN_KEY) === 'true';
      setWelcomeSeen(hasSeen);
      setShowWelcome(!hasSeen);
    } catch {
      setShowWelcome(true);
      setWelcomeSeen(false);
    }

    fetchCurrentUser()
      .then((currentUser) => {
        if (currentUser?.id && Number.isFinite(Number(currentUser.id))) {
          setCurrentUserId(Number(currentUser.id));
        }
        setIsAdmin(Boolean(currentUser?.is_admin));
      })
      .catch(() => {
        // Keep functionality working even if user fetch fails
      });
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

  const handleChatOpen = React.useCallback(() => {
    setChatOpen(true);
  }, []);

  const handleChatClose = React.useCallback(() => {
    setChatOpen(false);
  }, []);

  return (
    <>
      {showWelcome && (
        <PageWelcome onGetStarted={handleGetStarted} />
      )}
      
      {!showWelcome && (
        <>
          <FloatingWidget onOpen={handleChatOpen} />
          {chatOpen && (
            <div style={{ position: 'fixed', bottom: 100, right: 32, zIndex: 1000 }}>
              <div style={{
                background: 'rgba(255,255,255,0.98)',
                borderRadius: 24,
                boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
                padding: 0,
                minWidth: 360,
                maxWidth: 400,
              }}>
                <ChatInterface
                  onClose={handleChatClose}
                  pageContext={pageContext}
                  isAdmin={isAdmin}
                  currentUserId={currentUserId}
                />
              </div>
            </div>
          )}
        </>
      )}
    </>
  );
}

function renderAssistantPage() {
  const mount = document.getElementById('riskradar-assistant-page-welcome');
  if (mount) {
    const root = createRoot(mount);
    root.render(<AssistantPageWrapper />);
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
