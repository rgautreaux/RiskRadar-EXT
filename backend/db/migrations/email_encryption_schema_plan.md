# Schema Design Plan: Encrypted Email & Unique Constraints

## Objective
Update the `users` table to store encrypted email addresses and enforce uniqueness, supporting AES-256-GCM encryption and migration from plaintext.

## Current Schema (users table)
- id: Integer, primary key
- device_token: Text
- display_name: Text
- email: Text, unique
- password_hash: Text
- zip_code: Text
- latitude: Float

## Proposed Changes
1. **Encrypted Email Field**
   - Store encrypted email as binary or base64-encoded text.
   - Add a field for the initialization vector (IV) used in AES-GCM.
   - Example:
     - encrypted_email: Text or Binary
     - email_iv: Text or Binary

2. **Unique Constraint**
   - Enforce uniqueness on the encrypted_email field.
   - If deterministic encryption is used, uniqueness is straightforward.
   - If non-deterministic, consider storing a hash of the email for uniqueness checking.

3. **Migration Plan**
   - Add new fields to the table.
   - Migrate existing plaintext emails to encrypted format in batches.
   - Validate uniqueness and integrity after migration.

## Example Table Definition (SQLAlchemy)
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ...existing code...
    encrypted_email = Column(Text, unique=True)
    email_iv = Column(Text)
    ...existing code...
```


## Detailed Migration Steps
1. **Preparation**
   - Backup the entire users table and verify restore procedures.
   - Confirm all application code paths using the email field are identified and documented.
   - Prepare a staging environment with anonymized user data for dry-run testing.

2. **Schema Update**
   - Add `encrypted_email` (Text/Binary) and `email_iv` (Text/Binary) columns to the users table (nullable at first).
   - Optionally, add `email_hash` (Text, unique) if using non-deterministic encryption for uniqueness enforcement.

3. **Batch Migration**
   - For each user:
     - Encrypt the plaintext email using AES-256-GCM with a unique IV.
     - Store the encrypted email and IV in the new columns.
     - If using a hash for uniqueness, compute and store the hash.
   - Mark migrated rows for tracking (e.g., with a temporary migration_status column or migration log).

4. **Validation**
   - After each batch, verify:
     - All encrypted_email values are non-null and decrypt correctly.
     - No duplicate encrypted_email or email_hash values exist.
     - User login and registration flows work as expected in staging.

5. **Cutover**
   - Update application logic to use encrypted_email for all authentication and lookup operations.
   - Remove or restrict access to the plaintext email field in code.

6. **Cleanup**
   - Once validated in production, drop the old email column (or restrict access to admins only).
   - Remove any temporary migration columns or flags.

## Edge Cases & Rollback Notes
- Users with duplicate emails (should be blocked by unique constraint, but validate before migration).
- Emails with unusual/unicode characters (test encryption/decryption for all valid email formats).
- Partial migration/interrupted batch (ensure idempotency and ability to resume or rollback safely).
- If decryption fails during migration, log the error and skip the user (do not crash entire batch).
- Rollback: To revert, restore the backup or use the rollback script to repopulate the email field from decrypted values, then drop encrypted_email/email_iv columns.

## Integration Points & Open Questions
- **Backend Integration:**
  - Confirm encryption/decryption utilities and key management are implemented and tested by backend team before production migration.
  - Ensure all API endpoints and authentication logic are updated to use encrypted_email.
  - Coordinate with frontend for any changes in user profile/email display.
- **Infra/DevOps:**
  - Ensure secrets management (for encryption keys) is in place and documented.
  - Plan for key rotation and recovery procedures.
- **Open Questions:**
  - Will deterministic encryption or a hash be used for uniqueness enforcement?
  - What is the exact key management solution (env var, secrets manager, etc.)?
  - Are there any legacy integrations or third-party systems that require plaintext email access?
  - What is the user communication plan for this migration?

## Next Steps
- Review this plan with backend and security leads.
- Finalize migration/rollback scripts and test in staging.
- Document all procedures and update maintainers.
