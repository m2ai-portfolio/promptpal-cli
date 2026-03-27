# PromptPal CLI

A command-line tool for developers to store, version, retrieve, and diff prompts for LLM-powered agent frameworks. All prompts are encrypted at rest using Fernet symmetric encryption.

## Features

- **`promptpal init`** -- Initialize an encrypted prompt repository (SQLite-backed)
- **`promptpal add`** -- Store new versions of prompts with automatic version incrementing
- **`promptpal diff`** -- Compare any two prompt versions with unified diff output
- **STDIN support** -- Pipe prompt content directly (e.g., `cat prompt.txt | promptpal add myagent`)
- **Encryption at rest** -- All prompt content is encrypted via Fernet (PBKDF2-derived key from passphrase)

## Project Structure

```
promptpal-cli/
├── promptpal/
│   ├── cli.py          # Click CLI entry point (init, add, diff commands)
│   ├── core.py         # DB initialization, encryption/decryption, key derivation
│   ├── store.py        # CRUD operations (add_prompt, get_prompt, get_latest_version)
│   ├── models.py       # Pydantic model (PromptRecord)
│   ├── diff.py         # Unified diff generation between prompt versions
│   └── tests/          # Unit tests (CLI, store, diff)
├── pyproject.toml       # Package config, setuptools entry point
└── init.sh              # One-step setup script
```

## Prerequisites

- Python 3.11+
- pip

## Setup

```bash
# Option 1: Quick start
./init.sh

# Option 2: Manual install
python -m venv venv
source venv/bin/activate
pip install -e .
```

## Usage

```bash
# Initialize the prompt repository
promptpal init

# Add a prompt (inline)
promptpal add greeting --content "Hello, {name}! How can I help you today?"

# Add a prompt (from STDIN / file)
cat system_prompt.txt | promptpal add agent-v2

# Add another version of the same prompt
promptpal add greeting --content "Hi {name}, I'm your assistant. What do you need?"

# Compare the two most recent versions (default behavior)
promptpal diff greeting

# Compare specific versions
promptpal diff greeting --from 1 --to 2
```

### Versioning Behavior

Each prompt name maintains its own version counter starting at 1. Every `add` call for the same name auto-increments the version. The `diff` command defaults to comparing the two most recent versions when no `--from`/`--to` flags are provided.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PROMPTPASS` | Passphrase for encryption key derivation | Built-in fallback key |
| `PROMPTPATH` | Directory for the SQLite database | `~/.promptpal` |

### Security Notes on `PROMPTPASS`

- When `PROMPTPASS` is **not set**, PromptPal uses a hardcoded fallback key. This is acceptable for local development but provides no real confidentiality -- anyone with access to the source code can decrypt stored prompts.
- When `PROMPTPASS` **is set**, the passphrase is run through PBKDF2-HMAC-SHA256 (100,000 iterations) with a fixed salt to derive a Fernet key. This provides meaningful encryption at rest.
- The salt is fixed (`promptpal_salt_v1`), meaning the same passphrase always produces the same key. This is intentional for deterministic access but means the passphrase itself must be strong.
- For shared or production use, always set `PROMPTPASS` to a strong passphrase via your environment (e.g., in `~/.env.shared`).

## Tech Stack

- [Click](https://click.palletsprojects.com/) -- CLI framework
- [cryptography](https://cryptography.io/) -- Fernet encryption (PBKDF2 key derivation)
- [Pydantic](https://docs.pydantic.dev/) -- Data validation
- sqlite3 -- Local storage
- difflib -- Unified diff generation

## Running Tests

```bash
source venv/bin/activate
python -m pytest promptpal/tests/ -v
```

## License

MIT
