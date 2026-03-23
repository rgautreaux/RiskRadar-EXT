# ONBOARDING.md

## RiskRadar Frontend Onboarding Guide

Welcome to the RiskRadar mobile frontend! This guide will help new contributors get started, understand the design system, and follow best practices for UI/UX consistency.

---

### 1. Project Structure
- All mobile code is in `frontend/RiskRadar/`
- Shared primitives: `components/themed-text.tsx`, `components/themed-view.tsx`
- Design tokens: `constants/theme.ts`
- Assets: `assets/icons/`, `assets/images/`
- Docs: `docs/`

### 2. Design System
- All colors, typography, and spacing are sourced from theme tokens (see DESIGN_SYSTEM.md)
- Use ThemedText and ThemedView for all new UI
- Never hard-code colors or font sizes in screens/components

### 3. Adding New Screens/Components
- Use existing primitives and tokens
- Document new props and usage with JSDoc
- Add usage examples to DESIGN_SYSTEM.md if introducing new patterns

### 4. Testing & QA
- Run lint and TypeScript checks before PRs
- Use QA_CHECKLIST.md for manual validation
- Add test cases or mock data for new primitives/components

### 5. Asset Management
- Place new icons/images in the correct subfolder under assets/
- Update ASSET_MAP.md if adding new assets

### 6. Who Owns What?
- See UI/UX Styling Plan for file/component ownership
- Avoid editing teammate-owned files/routes/features without coordination

### 7. Further Reading
- DESIGN_SYSTEM.md (tokens, typography, asset usage)
- QA_CHECKLIST.md (manual QA)
- ASSET_MAP.md (asset mapping)
- UI_UX_STYLING_PLAN.md (implementation plan)

---

_Last updated: March 23, 2026_
