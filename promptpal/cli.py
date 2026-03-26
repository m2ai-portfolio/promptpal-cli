"""CLI interface for PromptPal."""

import click
import sys
from .core import init_db


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

    Placeholder for Feature 2 (not yet implemented).
    """
    click.echo(f"'add' command not yet implemented (name={name})")
    sys.exit(1)


@cli.command()
@click.argument("name")
@click.option("--from", "from_version", type=int, help="Starting version number")
@click.option("--to", "to_version", type=int, help="Ending version number")
def diff(name: str, from_version: int, to_version: int):
    """
    Show differences between two versions of a prompt.

    Placeholder for Feature 3 (not yet implemented).
    """
    click.echo(f"'diff' command not yet implemented (name={name})")
    sys.exit(1)


if __name__ == "__main__":
    cli()
