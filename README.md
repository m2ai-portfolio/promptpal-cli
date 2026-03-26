# PromptPal CLI

A command-line tool for developers to store, version, retrieve, and diff prompts for LLM-powered agent frameworks.

## Features
- **`promptpal init`** - Initialize encrypted prompt repository
- **`promptpal add`** - Store new versions of prompts with automatic versioning
- **`promptpal diff`** - Compare prompt versions with unified diff output

## Tech Stack
- Python 3.11+
- click (CLI framework)
- cryptography (Fernet encryption)
- sqlite3 (local storage)
- difflib (unified diffs)

## Setup
```bash
./init.sh
```

## Usage
```bash
# Initialize repository
PROMPTPASS=mysecret promptpal init

# Add a prompt
promptpal add greeting --content "Hello, {name}!"

# Compare versions
promptpal diff greeting
```

## Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| PROMPTPASS | Passphrase for encryption key | built-in fallback |
| PROMPTPATH | Database directory | ~/.promptpal |
