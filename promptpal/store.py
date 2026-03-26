"""Storage operations for prompts."""

import sqlite3
from datetime import datetime
from .core import get_db_connection, encrypt_content


def add_prompt(name: str, content: str) -> int:
    """
    Store a new version of a prompt.

    Args:
        name: The prompt name
        content: The plaintext content to store

    Returns:
        int: The new version number

    Raises:
        sqlite3.IntegrityError: If there's a database constraint violation
        FileNotFoundError: If database doesn't exist (user needs to run init)
    """
    # Get database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Look up the current max version for this prompt name
        cursor.execute(
            "SELECT MAX(version) FROM prompts WHERE name = ?",
            (name,)
        )
        result = cursor.fetchone()
        max_version = result[0] if result[0] is not None else 0

        # New version is max + 1
        new_version = max_version + 1

        # Encrypt the content
        encrypted_content = encrypt_content(content)

        # Generate ISO-8601 timestamp
        timestamp = datetime.utcnow().isoformat() + 'Z'

        # Insert the new prompt record
        cursor.execute(
            """
            INSERT INTO prompts (name, version, content, timestamp)
            VALUES (?, ?, ?, ?)
            """,
            (name, new_version, encrypted_content, timestamp)
        )

        conn.commit()
        return new_version

    except sqlite3.IntegrityError as e:
        conn.rollback()
        raise sqlite3.IntegrityError(f"Failed to store prompt: {e}") from e

    finally:
        conn.close()
