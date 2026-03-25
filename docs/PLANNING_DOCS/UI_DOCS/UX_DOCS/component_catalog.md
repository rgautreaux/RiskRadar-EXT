# RiskRadar Web Component Catalog

**Author:** Rebecca (Layout Lane)
**Last Updated:** 2026-03-23

## Purpose
This catalog documents all available layout and utility classes for the RiskRadar web app, with usage examples for each.

---

## Layout Classes
- `.flex-row`, `.flex-col`, `.align-center`, `.justify-between`, `.gap-xs`, `.gap-sm`, `.gap-md`, `.gap-lg`, `.gap-xl`

**Example:**
```html
<div class="flex-row align-center gap-md">
  <span>Item 1</span>
  <span>Item 2</span>
</div>
```

---

## Typography Classes
- `.text-xs`, `.text-sm`, `.text-md`, `.text-lg`, `.text-xl`, `.text-muted`, `.text-ink`

**Example:**
```html
<p class="text-lg text-muted">Muted large text</p>
```

---

## Color Utility Classes
- `.bg-coral`, `.bg-amber`, `.bg-teal`, `.bg-panel`, `.bg-panel-strong`

**Example:**
```html
<div class="bg-coral text-ink">Coral background</div>
```

---

## Icon Utility Classes
- `.icon-slot`, `.icon-badge`, `.nav-icon`

**Example:**
```html
<span class="icon-slot"><img src="/wireframe_icons/alerts.png" class="nav-icon" alt="Alerts"></span>
```

---

## Notes
- Only use these classes for global/shared layout and style.
- For new utility needs, propose additions to this catalog before using in templates.
