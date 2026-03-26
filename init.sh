#!/bin/bash
set -e

cd "$(dirname "$0")"

# Install Python dependencies
pip install click cryptography pydantic 2>/dev/null || pip install --user click cryptography pydantic 2>/dev/null

# Install the package in development mode
pip install -e . 2>/dev/null || pip install --user -e . 2>/dev/null

echo "PromptPal CLI is ready. Run 'promptpal --help' to get started."
