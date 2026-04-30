// Golby Onboarding Tutorial Logic (Web)

const steps = [
  "Hi, I'm <strong>Golby</strong>! Let's take a quick tour so you can get the most out of your dashboard. Click 'Next' to begin!",
  "This is your <strong>Dashboard</strong> — see live alerts, summaries, and trends at a glance!",
  "Check your <strong>Profile</strong> to update preferences and personalize your experience.",
  "Explore <strong>Alerts</strong> for detailed info on environmental risks in your area.",
  "That's it! You're ready to use RiskRadar. If you need help, Golby is always here!"
];

let currentStep = 0;

function showGolbyOnboarding() {
  const popup = document.getElementById('golby-onboarding-popup');
  const stepText = document.getElementById('golby-onboarding-step');
  const nextBtn = document.getElementById('golby-onboarding-next');
  const skipBtn = document.getElementById('golby-onboarding-skip');
  if (!popup || !stepText || !nextBtn || !skipBtn) return;
  popup.style.display = 'block';
  stepText.innerHTML = steps[currentStep];

  nextBtn.onclick = function() {
    currentStep++;
    if (currentStep < steps.length) {
      stepText.innerHTML = steps[currentStep];
      if (currentStep === steps.length - 1) {
        nextBtn.textContent = 'Finish';
      }
    } else {
      completeGolbyOnboarding();
    }
  };
  skipBtn.onclick = function() {
    completeGolbyOnboarding();
  };
}

function completeGolbyOnboarding() {
  const popup = document.getElementById('golby-onboarding-popup');
  popup.style.display = 'none';
  // Call backend to persist completion
  fetch('/components/golby/completeOnboarding.php', { method: 'POST', credentials: 'include' });
}

// Auto-trigger if needed (backend should inject a flag)
window.addEventListener('DOMContentLoaded', function() {
  if (window.GOLBY_ONBOARDING_NEEDED) {
    showGolbyOnboarding();
  }
});
