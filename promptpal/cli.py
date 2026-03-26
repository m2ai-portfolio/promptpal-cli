"""CLI interface for PromptPal."""

import click
import sys
from .core import init_db
from .store import add_prompt, get_prompt, get_latest_version
from .diff import diff_prompts


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """PromptPal - Version control for LLM prompts."""
    pass


@cli.command()
def init():
    """
    Initialize a new encrypted prompt repository.

    Creates the storage directory (PROMPTPATH, default ~/.promptpal)
    and SQLite database if they don't exist. Running init on an
    existing repository is a no-op.
    """
    try:
        already_exists, db_path = init_db()

        if already_exists:
            click.echo("Repository already initialized.")
        else:
            click.echo(f"Initialized PromptPal repository at {db_path}")

        sys.exit(0)

    except Exception as e:
        click.echo(f"Error initializing repository: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.option("--content", help="Prompt content (or read from STDIN if not provided)")
def add(name: str, content: str):
    """
    Store a new version of a prompt.

    Takes a prompt name and raw content (via --content option or STDIN).
    Increments the version number for that name, stores the encrypted content
    and an ISO-8601 timestamp.
    """
    try:
        # If --content not provided, read from STDIN
        if content is None:
            content = sys.stdin.read()

        # Validate that content is non-empty
        if not content or content.strip() == "":
            click.echo("Error: Prompt content cannot be empty", err=True)
            sys.exit(1)

        # Store the prompt
        version = add_prompt(name, content)

        # Print success message
        click.echo(f"Stored {name} v{version}")
        sys.exit(0)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("Run 'promptpal init' to initialize the repository first.", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Error storing prompt: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("name")
@click.option("--from", "from_version", type=int, default=None, help="Starting version number")
@click.option("--to", "to_version", type=int, default=None, help="Ending version number")
def diff(name: str, from_version: int, to_version: int):
    """
    Show differences between two versions of a prompt.

    Displays a unified diff between two versions. If neither --from nor --to
    is specified, compares the previous version to the latest. If only one is
    specified, the other defaults to the latest version.
    """
    try:
        # Get the latest version number for this prompt
        latest_version = get_latest_version(name)

        if latest_version is None:
            click.echo(f"Error: Prompt '{name}' not found", err=True)
            sys.exit(1)

        # Apply defaulting logic
        if from_version is None and to_version is None:
            # Neither specified: compare latest-1 to latest
            to_version = latest_version
            from_version = latest_version - 1 if latest_version > 1 else latest_version
        elif from_version is None:
            # Only --to specified: default --from to latest
            from_version = latest_version
        elif to_version is None:
            # Only --from specified: default --to to latest
            to_version = latest_version

        # Retrieve both versions
        prompt_from = get_prompt(name, from_version)
        prompt_to = get_prompt(name, to_version)

        # Check if versions exist
        if prompt_from is None:
            click.echo(f"Error: Version {from_version} of prompt '{name}' not found", err=True)
            sys.exit(1)

        if prompt_to is None:
            click.echo(f"Error: Version {to_version} of prompt '{name}' not found", err=True)
            sys.exit(1)

        # Generate diff
        diff_output = diff_prompts(
            prompt_from.content,
            prompt_to.content,
            name,
            from_version,
            to_version
        )

        # Print diff (or message if no differences)
        if diff_output:
            click.echo(diff_output)
        else:
            click.echo("No differences")

        sys.exit(0)

    except FileNotFoundError as e:
        click.echo(f"Error: {e}", err=True)
        click.echo("Run 'promptpal init' to initialize the repository first.", err=True)
        sys.exit(1)

    except Exception as e:
        click.echo(f"Error generating diff: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    cli()
