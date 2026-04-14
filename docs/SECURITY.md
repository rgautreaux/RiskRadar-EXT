# RiskRadar Security Notes

## User Email Protection

User email addresses are encrypted at rest before being written to the database. The application also stores a deterministic lookup hash so registration and duplicate checks can still operate without decrypting every row.

## Password Storage

Passwords are not encrypted. They are hashed with PBKDF2_SHA256 using the existing Passlib context. This is a one-way hash and is not reversible.

## Key Management

- Store `EMAIL_ENCRYPTION_KEY` outside version control.
- Prefer a secret manager or deployment-specific environment variables.
- Rotate keys through a controlled process and re-run the email migration if you need to re-encrypt historical values.

## Deployment Order

1. Back up the database.
2. Deploy the backend code.
3. Run the email migration script.
4. Apply the schema migration if the database still needs the `email_lookup_hash` column.
5. Verify registration and duplicate checks in a staging environment.

## Password Policy

The backend currently enforces a minimum password length and complexity rules during registration. Keep the policy aligned with your course or deployment security requirements.

## AI Assistant Guardrails

The Golby assistant is scoped to RiskRadar product guidance and environmental risk interpretation. It should not behave as a general-purpose advisory agent.

### In-Scope Responses

- Explain RiskRadar features, pages, alerts, forecast views, and risk map usage.
- Summarize live environmental risk/forecast data returned by project APIs.
- Provide non-authoritative, safety-first travel preparation suggestions tied to platform risk signals.

### Out-of-Scope Responses (Must Refuse or Redirect)

- Medical, legal, or emergency-response directives presented as professional advice.
- Harmful, illegal, or exploitative instructions.
- Requests for credentials, secrets, keys, or hidden system details.

### Required Fallback Behavior

- For emergency-risk prompts, direct users to local emergency services and official authorities.
- For medical/legal prompts, state limitations and recommend qualified professionals.
- Keep responses concise, non-alarmist, and avoid pretending to have real-time authority beyond API data.

### Validation Checklist

- Verify the assistant refuses disallowed prompt classes consistently.
- Verify fallback messages appear when live data fetches fail.
- Verify no secrets or internal implementation details are exposed in assistant responses.