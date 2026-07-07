import React from 'react';
import { FloatingWidget } from './FloatingWidget';
import { ChatInterface } from './ChatInterface';
import { WelcomeTab } from './WelcomeTab';
import { fetchCurrentUser } from './apiClient';
import { detectCurrentPage } from './pageContext';

const WELCOME_SEEN_KEY = 'golby-welcome-seen';

export function GolbyAssistantWidget() {
  const [open, setOpen] = React.useState(false);
  const [showWelcome, setShowWelcome] = React.useState(false);
  const [welcomeSeen, setWelcomeSeen] = React.useState(false);
  const [pageContext, setPageContext] = React.useState('unknown');
  const [currentUserId, setCurrentUserId] = React.useState<number | undefined>(undefined);
  const [isAdmin, setIsAdmin] = React.useState(false);

  React.useEffect(() => {
    try {
      const hasSeen = window.sessionStorage.getItem(WELCOME_SEEN_KEY) === 'true';
      setWelcomeSeen(hasSeen);
    } catch {
      setWelcomeSeen(false);
    }

    const detectedPage = detectCurrentPage();
    setPageContext(detectedPage);

    if (detectedPage === 'assistant') {
      setOpen(true);
      setShowWelcome(true);
    }

    const mount = document.getElementById('riskradar-ai-assistant-widget');

    const parsedCurrentUserId = Number(mount?.dataset.currentUserId ?? mount?.dataset.adminUserId);
    if (Number.isFinite(parsedCurrentUserId) && parsedCurrentUserId > 0) {
      setCurrentUserId(parsedCurrentUserId);
    }

    setIsAdmin(mount?.dataset.isAdmin === 'true');

    fetchCurrentUser()
      .then((currentUser) => {
        if (currentUser?.id && Number.isFinite(Number(currentUser.id))) {
          setCurrentUserId(Number(currentUser.id));
        }

        setIsAdmin(Boolean(currentUser?.is_admin));
      })
      .catch(() => {
        // Keep the server-rendered session state if the current user lookup fails.
      });
  }, []);

  const handleOpen = React.useCallback(() => {
    setOpen(true);
    setShowWelcome(!welcomeSeen);
  }, [welcomeSeen]);

  const handleGetStarted = React.useCallback(() => {
    setShowWelcome(false);
    setWelcomeSeen(true);
    try {
      window.sessionStorage.setItem(WELCOME_SEEN_KEY, 'true');
    } catch {
      // Ignore storage issues and keep chat usable.
    }
  }, []);

  const handleClose = React.useCallback(() => {
    setOpen(false);
  }, []);

  const panelStyle: React.CSSProperties = showWelcome
    ? {
        background: 'rgba(255,255,255,0.98)',
        borderRadius: 24,
        boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
        padding: 0,
        minWidth: 360,
        maxWidth: 720,
        maxHeight: '80vh',
        overflowY: 'auto',
      }
    : {
        background: 'rgba(255,255,255,0.98)',
        borderRadius: 24,
        boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
        padding: 0,
        minWidth: 360,
        maxWidth: 400,
      };

  return (
    <>
      <FloatingWidget onOpen={handleOpen} />
      {open && (
        <div style={{ position: 'fixed', bottom: 100, right: 32, zIndex: 1000 }}>
          <div style={panelStyle}>
            {showWelcome ? (
              <WelcomeTab onGetStarted={handleGetStarted} />
            ) : (
              <ChatInterface onClose={handleClose} pageContext={pageContext} isAdmin={isAdmin} currentUserId={currentUserId} />
            )}
          </div>
        </div>
      )}
    </>
  );
}
