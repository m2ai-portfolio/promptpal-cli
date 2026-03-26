"""Data models for PromptPal."""

from pydantic import BaseModel
from datetime import datetime


class PromptRecord(BaseModel):
    """Plain-text representation of a prompt as used internally."""
    name: str
    version: int
    content: str          # decrypted prompt text
    timestamp: datetime   # stored as ISO-8601 string in DB
