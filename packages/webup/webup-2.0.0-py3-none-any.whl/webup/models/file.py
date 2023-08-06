from dataclasses import dataclass
from pathlib import Path


@dataclass
class File:
    """
    A file to be uploaded.
    """

    key: str
    """
    S3 key.
    """

    path: Path
    """
    Local path.
    """
