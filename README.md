<p align="center">
  <img src="assets/infographic.png" alt="PromptPal CLI" width="800">
</p>

<h3 align="center">A single-binary command line tool that lets developers store, version, retrieve, and diff prompts for any agent framework. Prompts are kept in a local encrypted SQLite database with Git-style change logs, enabling CI/CD pipelines to test prompt changes safely.</h3>

<p align="center">
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#features">Features</a> &bull;
  <a href="#examples">Examples</a> &bull;
  <a href="#contributing">Contributing</a>
</p>

**What is this?**  
PromptPal CLI is a lightweight utility for developers who work with language model prompts. It provides versioned storage, retrieval, and diff capabilities so teams can track prompt evolution and reproduce agent behavior reliably.  
Example usage:

```
$ promptpal store --name "qa-assistant" --content "Answer the user's question concisely."
Stored prompt "qa-assistant" with ID 1
```

**Problem**  
Managing prompt versions across experiments is error‑prone; developers copy‑paste prompts into source files, causing drift and making reproducible agent behavior hard to achieve.

**Features**

| Feature | Description |
|---------|-------------|
| Encrypted storage | Prompts are saved in a local SQLite database protected with AES‑256 encryption. |
| Version control | Each save creates a new version with a Git‑style commit log, enabling history tracking. |
| Retrieve by name or ID | Fetch the latest prompt or a specific version using a simple lookup. |
| Diff comparisons | Show line‑by‑line changes between any two versions of a prompt. |
| List all prompts | View a summary of stored prompts with their latest version numbers. |
| Delete prompts | Remove a prompt and all its versions when no longer needed. |
| CI/CD friendly | The CLI returns non‑zero exit codes on failures, suitable for automated pipelines. |
| Plug‑in agnostic | Works with any agent framework because it stores plain‑text prompts only. |

**Quick Start**

1. Clone the repository  
   ```
   git clone https://github.com/yourorg/promptpal-cli.git
   ```
2. Change directory  
   ```
   cd promptpal-cli
   ```
3. Install the package in editable mode  
   ```
   pip install -e .
   ```
4. Verify the installation  
   ```
   promptpal --help
   ```
5. Store your first prompt  
   ```
   promptpal store --name "example" --content "Hello, world!"
   ```

**Examples**

**Store a new prompt**  
Command:  
```
promptpal store --name "summarizer" --content "Summarize the following paragraph:"
```
Output:  
```
Stored prompt "summarizer" with ID 1
```

**Update a prompt (creates a new version)**  
Command:  
```
promptpal store --name "summarizer" --content "Provide a brief summary of the text below:"
```
Output:  
```
Updated prompt "summarizer" to version 2
```

**Diff between two versions**  
Command:  
```
promptpal diff --name "summarizer" --from 1 --to 2
```
Output:  
```
--- v1 (ID:1)  
+++ v2 (ID:2)  
@@ -1 +1 @@  
-Summarize the following paragraph:  
+Provide a brief summary of the text below:
```

**File Structure**

```
PromptPal CLI/
├── promptpal/          # Core source code
│   ├── cli.py          # Command‑line interface built with Click
│   ├── core.py         # Orchestrates store, diff, and version logic
│   ├── diff.py         # Unified diff implementation for prompts
│   ├── models.py       # SQLAlchemy‑style models for Prompt and Version
│   └── store.py        # Encrypted SQLite wrapper (AES‑256 via cryptography)
├── tests/              # Test suite
│   ├── test_cli.py
│   ├── test_diff.py
│   └── test_store.py
├── assets/             # Documentation graphics
│   └── infographic.png
├── .gitignore
├── pyproject.toml      # Project metadata, dependencies, and build system
└── init.sh             # Optional setup script for development environments
```

**Tech Stack**

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Core language and runtime |
| Click | Declarative command‑line interface |
| SQLite3 | Embedded database for prompt storage |
| cryptography | AES‑256 encryption of the database file |
| difflib (std‑lib) | Generates prompt diffs |
| pytest | Test framework |

**Contributing**

1. Fork the repository.  
2. Create a feature branch.  
3. Run `pytest` to verify changes.  
4. Submit a pull request.

**License**

MIT

**Author**

```
Matthew Snow -- [M2AI](https://m2ai.co) | [@m2ai-portfolio](https://github.com/m2ai-portfolio)