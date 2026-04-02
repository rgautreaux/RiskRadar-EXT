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