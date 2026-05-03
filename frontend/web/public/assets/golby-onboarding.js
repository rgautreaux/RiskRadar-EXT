(function () {
  const config = window.__GOLBY_ONBOARDING__;
  if (!config || !config.user_id || !config.complete_url) {
    return;
  }

  const storageKey = `golby-onboarding-complete:${config.user_id}`;
  if (window.localStorage.getItem(storageKey) === '1') {
    return;
  }

  const shell = document.getElementById('golby-onboarding-shell');
  if (!shell) {
    return;
  }

  const dialog = shell.querySelector('[data-golby-onboarding-dialog]');
  const counter = shell.querySelector('[data-golby-onboarding-counter]');
  const title = shell.querySelector('[data-golby-onboarding-step-title]');
  const body = shell.querySelector('[data-golby-onboarding-step-body]');
  const progress = shell.querySelector('[data-golby-onboarding-progress]');
  const primary = shell.querySelector('[data-golby-onboarding-action="next"]');
  const skip = shell.querySelector('[data-golby-onboarding-action="skip"]');
  const dismissers = shell.querySelectorAll('[data-golby-onboarding-action="dismiss"], [data-golby-onboarding-dismiss="backdrop"]');

  if (!dialog || !counter || !title || !body || !progress || !primary || !skip) {
    return;
  }

  const pageLabel = String(config.page_label || 'this page');
  const steps = [
    {
      title: `Hi, I’m Golby. Welcome to ${pageLabel}`,
      body: 'You’ve just landed in the right place. I’ll guide you through the most helpful parts of RiskRadar so your new account feels friendly, calm, and easy to use.',
    },
    {
      title: 'Start with the big picture',
      body: 'Your Dashboard and Alerts pages are the fastest way to spot what is happening right now. Golby keeps the important stuff clear so you can relax and move at your own pace.',
    },
    {
      title: 'Make the app feel like yours',
      body: 'The Profile page lets you update preferences, ZIP code, and notification settings so the experience stays personal and useful as you explore.',
    },
    {
      title: 'You’re ready to go',
      body: 'That’s the quick tour. You can come back to these pages any time, and Golby will still be here to help when you need a hand.',
    },
  ];

  let currentStep = 0;
  let isCompleting = false;

  function setOpen(open) {
    shell.hidden = !open;
    document.body.classList.toggle('golby-onboarding-open', open);
  }

  function renderStep() {
    const step = steps[currentStep];
    title.textContent = step.title;
    body.textContent = step.body;
    counter.textContent = `Step ${currentStep + 1} of ${steps.length}`;
    progress.style.width = `${((currentStep + 1) / steps.length) * 100}%`;
    primary.textContent = currentStep === steps.length - 1 ? 'Finish tour' : 'Next';
    primary.setAttribute('aria-label', primary.textContent);
  }

  async function completeOnboarding() {
    if (isCompleting) {
      return;
    }

    isCompleting = true;
    primary.disabled = true;
    skip.disabled = true;

    try {
      const response = await fetch(config.complete_url, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ completed: true }),
      });

      if (!response.ok) {
        throw new Error('Failed to persist onboarding completion');
      }

      window.localStorage.setItem(storageKey, '1');
    } catch (error) {
      console.warn('Golby onboarding completion could not be saved', error);
    } finally {
      setOpen(false);
    }
  }

  function goNext() {
    if (currentStep === steps.length - 1) {
      void completeOnboarding();
      return;
    }

    currentStep += 1;
    renderStep();
  }

  function handleKeydown(event) {
    if (event.key === 'Escape') {
      event.preventDefault();
      void completeOnboarding();
      return;
    }

    if (event.key === 'Tab') {
      const focusable = Array.from(
        shell.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')
      ).filter((element) => !element.hasAttribute('disabled'));

      if (!focusable.length) {
        return;
      }

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }
  }

  setOpen(true);
  renderStep();
  primary.addEventListener('click', goNext);
  skip.addEventListener('click', () => void completeOnboarding());
  dismissers.forEach((element) => {
    element.addEventListener('click', () => void completeOnboarding());
  });
  dialog.addEventListener('keydown', handleKeydown);
  window.addEventListener('keydown', handleKeydown);
  window.setTimeout(() => {
    primary.focus();
  }, 0);
})();