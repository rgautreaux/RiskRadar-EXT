import React from 'react';
import { FloatingWidget } from './FloatingWidget';
import { ChatInterface } from './ChatInterface';
import { fetchCurrentUser } from './apiClient';
import { detectCurrentPage } from './pageContext';

export function GolbyAssistantWidget() {
  const [open, setOpen] = React.useState(false);
  const [pageContext, setPageContext] = React.useState('unknown');
  const [currentUserId, setCurrentUserId] = React.useState<number | undefined>(undefined);
  const [isAdmin, setIsAdmin] = React.useState(false);

  React.useEffect(() => {
    const detectedPage = detectCurrentPage();
    setPageContext(detectedPage);

    if (detectedPage === 'assistant') {
      setOpen(true);
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

  return (
    <>
      <FloatingWidget onOpen={() => setOpen(true)} />
      {open && (
        <div style={{ position: 'fixed', bottom: 100, right: 32, zIndex: 1000 }}>
          <div style={{ background: 'rgba(255,255,255,0.98)', borderRadius: 24, boxShadow: '0 8px 32px rgba(0,0,0,0.18)', padding: 0, minWidth: 360, maxWidth: 400 }}>
            <ChatInterface onClose={() => setOpen(false)} pageContext={pageContext} isAdmin={isAdmin} currentUserId={currentUserId} />
          </div>
        </div>
      )}
    </>
  );
}
