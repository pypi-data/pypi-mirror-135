from functools import cached_property
from os import walk
from pathlib import Path
from typing import Iterator

from webup.models import File


class Files:
    """
    Iterates over the local files and directories to upload.

    Arguments:
        dir: Path to root local directory to upload.
    """

    def __init__(self, dir: str | Path) -> None:
        self._dir = dir
        self._iterator = self.iterator(dir)

    @staticmethod
    def iterator(dir: str | Path) -> Iterator[File]:
        """
        Creates and returns an iterator for a directory.

        The iterator will include subdirectories and their children. There is no
        need to invoke this function recursively.

        Arguments:
            dir: Path to root local directory.
        """

        for root, _, files in walk(dir):
            root_path = Path(root)
            for filename in files:
                path = root_path / filename
                key = path.relative_to(dir).as_posix()
                yield File(path=path, key=key)

    @cached_property
    def max_path(self) -> int:
        """
        Gets the maximum path length.
        """

        best = 0
        for file in self.iterator(self._dir):
            best = max(best, len(file.path.as_posix()))
        return best

    @property
    def next(self) -> File | None:
        """
        Gets the next file to upload, or `None` when there are no more.
        """

        try:
            return next(self._iterator)
        except StopIteration:
            return None
