from pathlib import Path
from re import match
from typing import Dict

_max_ages: Dict[str, int] = {}

_default_max_age = -1


def set_default_maximum_age(seconds: int = 60) -> None:
    """
    Sets the Cache-Control "max-age" value for files not registered via
    `set_maximum_age`.

    Defaults to 60 seconds.
    """

    global _default_max_age
    _default_max_age = seconds


def cache_control(path: Path) -> str:
    """
    Gets the Cache-Control header for a file.
    """

    return f"max-age={max_age(path)}"


def max_age(path: Path) -> int:
    """
    Gets the maximum age in seconds for a file.
    """

    posix = path.as_posix()

    for pattern in _max_ages:
        if match(pattern, posix):
            return _max_ages[pattern]

    return _default_max_age


def set_maximum_age(pattern: str, seconds: int) -> None:
    """
    Sets the "max-age" value of the Cache-Control header for files that match
    the given pattern.
    """

    _max_ages[pattern] = seconds


set_default_maximum_age()
