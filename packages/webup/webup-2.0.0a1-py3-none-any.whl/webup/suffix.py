def normalize_suffix(suffix: str) -> str:
    """
    Normalises a filename suffix for lookups.

    Arguments:
        suffix: Filename suffix.
    """

    suffix = suffix.lower().strip()
    if suffix.startswith("."):
        suffix = suffix[1:]
    return suffix
