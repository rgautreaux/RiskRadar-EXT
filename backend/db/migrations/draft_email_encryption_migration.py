
"""
Draft Migration Script: Email Encryption & Unique Constraint

SAFE FOR TEST/STAGING ONLY. Do NOT execute in production. Use only with test or anonymized data.
This script is for planning and validation of migration logic. It is designed to be idempotent and safe for repeated runs in a test environment.
"""


from sqlalchemy import Column, Text, MetaData, Table
from sqlalchemy.engine import create_engine
from sqlalchemy.exc import ProgrammingError
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import os


# Example connection string (update as needed)
DATABASE_URL = "mysql+pymysql://user:password@localhost/riskradar_db"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

users = Table("users", metadata, autoload_with=engine)


# Example: AES-GCM encryption function (for test only; use a fixed key in test env)
def encrypt_email(email, key):
    iv = os.urandom(12)
    aesgcm = AESGCM(key)
    encrypted = aesgcm.encrypt(iv, email.encode(), None)
    return base64.b64encode(encrypted).decode(), base64.b64encode(iv).decode()


# Migration steps (test/staging only, idempotent):
# 1. Add new columns: encrypted_email, email_iv (if not already present)
# 2. For each user, if encrypted_email is NULL, encrypt the email and store in new columns
# 3. Validate uniqueness of encrypted_email (raise error if duplicates found)
# 4. Do NOT drop old email column in test runs; only after full validation

# Example migration logic (not executable, for planning):
# with engine.connect() as conn:
#     # Step 1: Add columns if not present
#     try:
#         conn.execute("ALTER TABLE users ADD COLUMN encrypted_email TEXT")
#     except ProgrammingError:
#         pass  # Column already exists
#     try:
#         conn.execute("ALTER TABLE users ADD COLUMN email_iv TEXT")
#     except ProgrammingError:
#         pass
#     # Step 2: Encrypt emails for users not yet migrated
#     for user in conn.execute(users.select()):
#         if not user.encrypted_email:
#             encrypted, iv = encrypt_email(user.email, key)
#             conn.execute(users.update().where(users.c.id == user.id).values(encrypted_email=encrypted, email_iv=iv))
#     # Step 3: Validate uniqueness
#     # (Pseudo: check for duplicate encrypted_email values)
#     # Step 4: (Optional) conn.execute("ALTER TABLE users ADD UNIQUE (encrypted_email)")
#     # Step 5: (Do NOT drop email column in test)

# All steps should be logged and validated in a test/staging environment only.
# This script is safe to re-run: it will skip already-migrated users and not fail if columns exist.
# Document all steps and results for review before any production use.
