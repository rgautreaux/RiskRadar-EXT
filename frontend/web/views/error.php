<?php rr_render_layout_start('Error', 'dashboard'); ?>

<style>
  /* ── Error page ──────────────────────────────────── */
  .error-scene {
    min-height: calc(68vh - 80px);
    display: grid;
    place-items: center;
    padding: 56px 24px;
    background:
      radial-gradient(circle at 50% 36%, oklch(0.54 0.15 148 / 0.06) 0%, transparent 62%),
      linear-gradient(180deg, rgba(255, 235, 214, 0.82), var(--panel, rgba(255, 246, 234, 0.92)));
  }

  .error-inner {
    max-width: 460px;
    width: 100%;
    text-align: center;
  }

  /* Topographic rings */
  .error-topo {
    width: 136px;
    height: 136px;
    margin: 0 auto 36px;
    display: block;
    overflow: visible;
  }

  .topo-ring {
    fill: none;
    stroke: oklch(0.54 0.15 148);
  }

  .topo-inner-lg {
    fill: oklch(0.54 0.15 148);
    opacity: 0.13;
  }

  .topo-inner-md {
    fill: oklch(0.54 0.15 148);
    opacity: 0.22;
  }

  .topo-center-dot {
    fill: oklch(0.54 0.15 148);
    opacity: 0.75;
    transform-box: fill-box;
    transform-origin: center;
  }

  /* Status badge */
  .error-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 4px 12px 4px 10px;
    border-radius: 999px;
    background: oklch(0.93 0.035 148);
    border: 1px solid oklch(0.80 0.075 148);
    font-family: 'Geist Mono', monospace;
    font-size: 0.67rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: oklch(0.41 0.14 148);
    margin: 0 0 20px;
  }

  .error-badge-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: oklch(0.54 0.15 148);
    flex-shrink: 0;
  }

  /* Heading */
  .error-heading {
    font-family: 'Bricolage Grotesque', system-ui, sans-serif;
    font-size: clamp(1.8rem, 5vw, 2.45rem);
    font-weight: 700;
    letter-spacing: -0.025em;
    line-height: 1.1;
    color: var(--ink, #122231);
    margin: 0 0 14px;
  }

  /* Body */
  .error-message {
    font-family: 'Atkinson Hyperlegible', sans-serif;
    font-size: 1rem;
    line-height: 1.65;
    color: var(--muted, #33485d);
    max-width: 42ch;
    margin: 0 auto 32px;
  }

  /* Return button */
  .btn-return {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 13px 22px;
    border-radius: 14px;
    background: oklch(0.54 0.15 148);
    color: oklch(0.97 0.015 148);
    font-family: 'Bricolage Grotesque', system-ui, sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    text-decoration: none;
    transition:
      transform 0.16s cubic-bezier(0.33, 1, 0.68, 1),
      box-shadow 0.16s cubic-bezier(0.33, 1, 0.68, 1);
  }

  .btn-return:hover,
  .btn-return:focus-visible {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px oklch(0.54 0.15 148 / 0.28);
  }

  .btn-return:focus-visible {
    outline: 2px solid oklch(0.54 0.15 148);
    outline-offset: 3px;
  }

  .btn-arrow {
    width: 14px;
    height: 14px;
    stroke: currentColor;
    stroke-width: 2.2;
    stroke-linecap: round;
    stroke-linejoin: round;
    fill: none;
    flex-shrink: 0;
  }

  /* Animations */
  @media (prefers-reduced-motion: no-preference) {
    .error-inner {
      animation: error-rise 0.55s cubic-bezier(0.33, 1, 0.68, 1) both;
    }

    .topo-center-dot {
      animation: dot-pulse 2.8s ease-in-out infinite;
    }

    @keyframes error-rise {
      from {
        opacity: 0;
        transform: translateY(16px);
      }
    }

    @keyframes dot-pulse {
      0%, 100% { opacity: 0.75; transform: scale(1); }
      50%       { opacity: 0.3;  transform: scale(0.65); }
    }
  }

  @media (max-width: 480px) {
    .error-scene {
      padding: 40px 16px;
    }

    .error-topo {
      width: 108px;
      height: 108px;
      margin-bottom: 28px;
    }
  }
</style>

<section class="panel error-scene">
  <div class="error-inner">

    <svg class="error-topo" viewBox="0 0 136 136" fill="none"
         xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <circle class="topo-ring" cx="68" cy="68" r="64" stroke-width="1"   opacity="0.08"/>
      <circle class="topo-ring" cx="68" cy="68" r="53" stroke-width="1"   opacity="0.15"/>
      <circle class="topo-ring" cx="68" cy="68" r="42" stroke-width="1.5" opacity="0.23"/>
      <circle class="topo-ring" cx="68" cy="68" r="31" stroke-width="1.5" opacity="0.35"/>
      <circle class="topo-ring" cx="68" cy="68" r="20" stroke-width="2"   opacity="0.5"/>
      <circle class="topo-inner-lg"   cx="68" cy="68" r="11"/>
      <circle class="topo-inner-md"   cx="68" cy="68" r="6"/>
      <circle class="topo-center-dot" cx="68" cy="68" r="2.8"/>
    </svg>

    <p class="error-badge" role="status">
      <span class="error-badge-dot" aria-hidden="true"></span>
      Request status
    </p>

    <h1 class="error-heading"><?php echo e($errorTitle ?? 'Something went wrong'); ?></h1>
    <p class="error-message"><?php echo e($errorMessage ?? 'The request could not be completed.'); ?></p>

    <a class="btn-return" href="index.php">
      <svg class="btn-arrow" viewBox="0 0 14 14" aria-hidden="true">
        <path d="M9.5 11 L4.5 7 L9.5 3"/>
      </svg>
      Return to dashboard
    </a>

  </div>
</section>

<?php rr_render_layout_end(); ?>
