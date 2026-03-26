"""Diff operations for comparing prompt versions."""

import difflib


def diff_prompts(content_from: str, content_to: str, name: str, version_from: int, version_to: int) -> str:
    """
    Generate a unified diff between two versions of a prompt.

    Args:
        content_from: The content of the starting version
        content_to: The content of the ending version
        name: The prompt name (used in diff headers)
        version_from: The starting version number
        version_to: The ending version number

    Returns:
        str: Unified diff string (empty if no differences)
    """
    # Split content into lines for difflib
    from_lines = content_from.splitlines(keepends=True)
    to_lines = content_to.splitlines(keepends=True)

    # Generate unified diff
    diff_lines = difflib.unified_diff(
        from_lines,
        to_lines,
        fromfile=f"{name} v{version_from}",
        tofile=f"{name} v{version_to}",
        lineterm=''
    )

    # Join the diff lines
    return '\n'.join(diff_lines)
