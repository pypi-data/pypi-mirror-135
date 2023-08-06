from typing import Dict

from webup.suffix import normalize_suffix

_content_types: Dict[str, str] = {}
_default_content_type = ""


def set_default_content_type(type: str = "application/octet-stream") -> None:
    """
    Sets the default Content-Type header for file types not registered via
    `set_content_type`.

    Defaults to "application/octet-stream".
    """

    global _default_content_type
    _default_content_type = type


def content_type(suffix: str) -> str:
    """
    Gets the Content-Type header for a type of file.

    Arguments:
        suffix: Filename suffix.
    """

    suffix = normalize_suffix(suffix)
    return _content_types.get(suffix, _default_content_type)


def set_content_type(suffix: str, type: str) -> None:
    """
    Registers the Content-Type header for files with the `suffix` filename
    extension.
    """

    suffix = normalize_suffix(suffix)
    _content_types[suffix] = type


set_default_content_type()

# TODO: Update the `__init__.py` documentation if you change these defaults:
set_content_type("css", "text/css")
set_content_type("eot", "application/vnd.m-fontobject")
set_content_type("html", "text/html")
set_content_type("js", "text/javascript")
set_content_type("png", "image/png")
set_content_type("ttf", "font/ttf")
set_content_type("woff", "font/woff")
set_content_type("woff2", "font/woff2")
