<p align="center">
  <img src="assets/infographic.png" alt="PromptPal CLI" width="800">
</p>

<h3 align="center">A single‑binary command line tool that lets developers store, version, retrieve, and diff prompts for any agent framework. Prompts are kept in a local encrypted SQLite database with Git‑style change logs, enabling CI/CD pipelines to test prompt changes safely.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

## What is this?
PromptPal CLI is a single‑binary utility that helps AI developers manage prompt versions locally. It stores prompts in an encrypted SQLite database, tracks changes like Git, and lets you retrieve or compare any version with simple commands.

```
$ promptpal add "Summarize article" --content "Provide a concise summary of the given text."
Prompt 'Summarize article' stored with ID: a1b2c3d4
```

## Problem
Managing prompt versions across experiments is error‑prone; developers copy‑paste prompts into source files, causing drift and making reproducible agent behavior hard to achieve.

## Features
| Feature | Description |
|---------|-------------|
| Encrypted storage | Prompts are saved in a local SQLite database protected by a user‑defined passphrase. |
| Git‑style versioning | Each save creates a new revision with a hash, enabling log, checkout, and diff operations. |
| Prompt retrieval | Fetch any prompt by name, ID, or revision using flexible query options. |
| Diff tool | Compare two prompt revisions side‑by‑side with highlighted changes. |
| CLI‑first design | All functionality accessible via a single binary with intuitive subcommands. |
| CI/CD friendly | Deterministic output and export hooks allow automated testing of prompt changes. |
| Passphrase rotation | Update the encryption key without re‑importing existing prompts. |
| Plugin‑ready core | Core logic isolated in `core.py` and `store.py` for easy extension. |

## Quick Start
1. Clone the repository  
   ```bash
   git clone https://github.com/yourorg/promptpal-cli.git
   cd promptpal-cli
   ```
2. Install the binary (requires Python 3.9+)  
   ```bash
   pip install -e .
   ```
3. Initialize your prompt store (you will be prompted for a passphrase)  
   ```bash
   promptpal init
   ```
4. Store your first prompt  
   ```bash
   promptpal add "Translate to French" --content "Translate the following English sentence to French."
   ```
   Example output:  
   ```
   Prompt 'Translate to French' stored with ID: 9f8e7d6c
   ```

## Examples
**Store a new prompt version**  
```
$ promptpal add "Translate to French" --content "Translate the following English sentence to French."
Prompt 'Translate to French' stored with ID: 9f8e7d6c (v1)
```
**Add an updated version of the same prompt**  
```
$ promptpal add "Translate to French" --content "Translate the provided English sentence into French, preserving tone."
Prompt 'Translate to French' stored with ID: 9f8e7d6c (v2)
```
**List all revisions for a prompt**  
```
$ promptpal log "Translate to French"
ID: 9f8e7d6c
  v1: 2025-09-16 10:12:03 | Translate the following English sentence to French.
  v2: 2025-09-16 10:15:41 | Translate the provided English sentence into French, preserving tone.
```
**Diff two revisions**  
```
$ promptpal diff 9f8e7d6c@v1 9f8e7d6c@v2
--- v1
+++ v2
@@ -1 +1 @@
-Translate the following English sentence to French.
+Translate the provided English sentence into French, preserving tone.
```
**Retrieve the latest version for use in a script**  
```
$ promptpal get latest --name "Translate to French" --format plain
Translate the provided English sentence into French, preserving tone.
```

## File Structure
```
PromptPal CLI/
  promptpal/          # Core source code
    __init__.py
    cli.py           # Command‑line interface entry point
    core.py          # Business logic for versioning and encryption
    store.py         # SQLite storage layer with AES‑256 encryption
    diff.py          # Side‑by‑side diff implementation
    models.py        # Data classes for Prompt and Revision
    tests/           # Unit tests
      __init__.py
      test_cli.py
      test_diff.py
      test_store.py
  .gitignore
  pyproject.toml     # Build metadata and dependencies
  init.sh            # Helper script for dev environment setup
  README.md
```

## Tech Stack
| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Language runtime |
| SQLite | Embedded encrypted database |
| cryptography library | AES‑256 encryption of prompts |
| Click | CLI framework for subcommands |
| Pytest | Test suite runner |
| Git‑style hashing (SHA‑256) | Revision identifiers |

## Contributing
Fork the repo, make your changes, run the test suite with `pytest`, then open a pull request. Ensure all tests pass and follow the existing code style.

## License
MIT

## Author
```
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)