# Demo/Test Script: Risk Score Breakdown & Accessibility

## Purpose
Demonstrate and verify the risk score breakdown UI, accessibility, and explainability for alerts.

## Steps

1. **Login as a registered user**
   - Go to `/login.php` and sign in with a test account.

2. **Navigate to Alerts**
   - Go to `/alerts.php` and select any alert to view its details.

3. **View Risk Score Breakdown**
   - On the alert detail page, scroll to the "Risk Score Breakdown" section.
   - Confirm that the risk score, level, and all factor scores are visible.
   - Expand the "How is this risk score calculated?" details for the formula and weights.

4. **Accessibility Checks**
   - Use keyboard navigation (Tab/Shift+Tab) to reach the risk score section and expand/collapse the formula details.
   - Use a screen reader to verify that headings, lists, and details are announced correctly.
   - Confirm that color contrast is sufficient for all text and backgrounds.

5. **Personalization Test**
   - Go to `/profile.php` and update your location, health conditions, or alert preferences.
   - Return to an alert detail page and verify that the risk score/factors update accordingly.

6. **Guest User Test**
   - Log out and repeat steps 2-4 as a guest. Confirm that a message is shown if risk breakdown is unavailable.

## Expected Results
- All users see a clear, accessible risk score breakdown for each alert (if logged in).
- The formula and factor weights are transparent and easy to understand.
- The UI is fully keyboard and screen reader accessible.
- Color contrast meets accessibility standards.
- Personalization is reflected in risk scores and factors.

---

Repeat for multiple alerts and user profiles to verify robustness.