"""Helper functions."""


from __future__ import annotations


def truncate(string: str, size: int = 50) -> str:
    """Truncate a string.

    Args:
        string (str): the string to operate on.
        size (int, optional): the size of the final string. Defaults to 50.

    Returns:
        str: the trucated string.
    """
    return string[: size - 3] + "..." if len(string) > size else string
