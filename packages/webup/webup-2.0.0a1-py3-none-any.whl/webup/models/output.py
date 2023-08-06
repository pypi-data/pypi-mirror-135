from dataclasses import dataclass
from typing import IO


@dataclass
class Output:
    max_path: int
    out: IO[str]
