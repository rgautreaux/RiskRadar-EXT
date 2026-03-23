
"""
Draft Rollback Script: Email Encryption Migration

SAFE FOR TEST/STAGING ONLY. Do NOT execute in production. Use only with test or anonymized data.
This script is for planning and validation of rollback logic. It is designed to be idempotent and safe for repeated runs in a test environment.
"""


from sqlalchemy.engine import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import ProgrammingError

# Example connection string (update as needed)
DATABASE_URL = "mysql+pymysql://user:password@localhost/riskradar_db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table("users", metadata, autoload_with=engine)


# Rollback steps (test/staging only, idempotent):
# 1. Add email column if not present
# 2. For each user, if email is NULL and encrypted_email is present, decrypt and restore email
# 3. Do NOT drop encrypted_email/email_iv columns in test runs; only after full validation

# Example rollback logic (not executable, for planning):
# with engine.connect() as conn:
#     # Step 1: Add email column if not present
#     try:
#         conn.execute("ALTER TABLE users ADD COLUMN email TEXT")
#     except ProgrammingError:
#         pass  # Column already exists
#     # Step 2: Decrypt and restore email for users not yet rolled back
#     for user in conn.execute(users.select()):
#         if not user.email and user.encrypted_email:
#             email = decrypt_email(user.encrypted_email, user.email_iv, key)
#             conn.execute(users.update().where(users.c.id == user.id).values(email=email))
#     # Step 3: (Do NOT drop encrypted_email/email_iv columns in test)

# All steps should be logged and validated in a test/staging environment only.
# This script is safe to re-run: it will skip already-rolled-back users and not fail if columns exist.
# Document all steps and results for review before any production use.
