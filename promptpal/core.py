"""Core database and encryption utilities for PromptPal."""

import os
import sqlite3
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet


# Fallback key for when PROMPTPASS is not set
# In production, this should be randomly generated and stored securely
FALLBACK_KEY = b"ZmFsbGJhY2tfa2V5X2Zvcl9wcm9tcHRwYWxfZGV2ZWxvcG1lbnQ="


def get_encryption_key() -> bytes:
    """
    Derive encryption key from PROMPTPASS environment variable.
    If PROMPTPASS is not set or empty, use a built-in fallback key.

    Returns:
        bytes: Fernet-compatible encryption key (base64-encoded 32 bytes)
    """
    passphrase = os.environ.get("PROMPTPASS", "").strip()

    if not passphrase:
        # Use fallback key
        return FALLBACK_KEY

    # Derive key from passphrase using PBKDF2
    # Use a fixed salt for deterministic key derivation from the same passphrase
    salt = b"promptpal_salt_v1"
    kdf_output = hashlib.pbkdf2_hmac(
        'sha256',
        passphrase.encode('utf-8'),
        salt,
        iterations=100000,
        dklen=32
    )
    # Fernet requires base64-encoded key
    return base64.urlsafe_b64encode(kdf_output)


def get_cipher() -> Fernet:
    """
    Get Fernet cipher instance with the current encryption key.

    Returns:
        Fernet: Cipher instance for encryption/decryption
    """
    key = get_encryption_key()
    return Fernet(key)


def get_db_path() -> Path:
    """
    Get the path to the SQLite database from PROMPTPATH environment variable.
    Defaults to ~/.promptpal if not set.

    Returns:
        Path: Absolute path to the database directory
    """
    prompt_path = os.environ.get("PROMPTPATH", "").strip()

    if not prompt_path:
        prompt_path = os.path.expanduser("~/.promptpal")
    else:
        # Expand ~ in the path if present
        prompt_path = os.path.expanduser(prompt_path)

    return Path(prompt_path)


def get_db_connection() -> sqlite3.Connection:
    """
    Get a connection to the PromptPal database.

    Returns:
        sqlite3.Connection: Database connection

    Raises:
        sqlite3.Error: If connection fails
    """
    db_path = get_db_path() / "promptpal.db"

    if not db_path.exists():
        raise FileNotFoundError(f"Database not found at {db_path}. Run 'promptpal init' first.")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> tuple[bool, str]:
    """
    Initialize the PromptPal database and directory structure.
    Creates PROMPTPATH directory and promptpal.db if they don't exist.

    Returns:
        tuple[bool, str]: (already_exists, db_path)
            - already_exists: True if DB already existed, False if newly created
            - db_path: Absolute path to the database file
    """
    db_dir = get_db_path()
    db_file = db_dir / "promptpal.db"

    # Check if database already exists
    already_exists = db_file.exists()

    if already_exists:
        return True, str(db_file)

    # Create directory if it doesn't exist
    db_dir.mkdir(parents=True, exist_ok=True)

    # Create database and table
    conn = sqlite3.connect(str(db_file))
    cursor = conn.cursor()

    # Create prompts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            version INTEGER NOT NULL,
            content BLOB NOT NULL,
            timestamp TEXT NOT NULL,
            UNIQUE(name, version)
        )
    """)

    # Create index for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_prompts_name_version
        ON prompts(name, version DESC)
    """)

    conn.commit()
    conn.close()

    return False, str(db_file)


def encrypt_content(plaintext: str) -> bytes:
    """
    Encrypt plaintext content using the repository encryption key.

    Args:
        plaintext: The content to encrypt

    Returns:
        bytes: Encrypted content
    """
    cipher = get_cipher()
    return cipher.encrypt(plaintext.encode('utf-8'))


def decrypt_content(ciphertext: bytes) -> str:
    """
    Decrypt encrypted content using the repository encryption key.

    Args:
        ciphertext: The encrypted content

    Returns:
        str: Decrypted plaintext content

    Raises:
        cryptography.fernet.InvalidToken: If decryption fails (wrong key or corrupted data)
    """
    cipher = get_cipher()
    return cipher.decrypt(ciphertext).decode('utf-8')
