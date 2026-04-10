import React from 'react';
import { createRoot } from 'react-dom/client';
import { FloatingWidget } from '../../components/golby/FloatingWidget';
import { ChatInterface } from '../../components/golby/ChatInterface';
import { detectCurrentPage } from '../../components/golby/pageContext';
import { WelcomeTab } from '../../components/golby/WelcomeTab';

function GolbyAssistantWidget() {
  const [open, setOpen] = React.useState(false);
  const [pageContext, setPageContext] = React.useState('unknown');
  const [isAdmin, setIsAdmin] = React.useState(false);

  React.useEffect(() => {
    setPageContext(detectCurrentPage());
    const mount = document.getElementById('riskradar-ai-assistant-widget');
    setIsAdmin(mount?.dataset.admin === 'true');
  }, []);

  return (
    <>
      <FloatingWidget onOpen={() => setOpen(true)} />
      {open && (
        <div style={{ position: 'fixed', bottom: 100, right: 32, zIndex: 1000 }}>
          <div style={{ background: 'rgba(255,255,255,0.98)', borderRadius: 24, boxShadow: '0 8px 32px rgba(0,0,0,0.18)', padding: 0, minWidth: 360, maxWidth: 400 }}>
            <ChatInterface onClose={() => setOpen(false)} pageContext={pageContext} isAdmin={isAdmin} />
          </div>
        </div>
      )}
    </>
  );
}

const mount = document.getElementById('riskradar-ai-assistant-widget');
if (mount) {
  const root = createRoot(mount);
  root.render(<GolbyAssistantWidget />);
}
