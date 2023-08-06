from dataclasses import dataclass


@dataclass
class UploadResult:
    bucket: str
    key: str
    path: str
    exception: Exception | None = None
