from logging import getLogger
from multiprocessing import Queue
from pathlib import Path
from queue import Empty
from typing import IO, List

from webup.cache_control import cache_control
from webup.content_type import content_type
from webup.files import Files
from webup.models import Output, UploadResult
from webup.session import make_session
from webup.ssm import get_ssm_value
from webup.upload_process import Upload

_logger = getLogger("webup")


def bucket_name(bucket: str | None, ssm_param: str | None, region: str | None) -> str:
    if bucket:
        return bucket

    if not ssm_param:
        raise ValueError("Either bucket or ssm_param must be set.")

    session = make_session(region)
    return get_ssm_value(ssm_param, session)


def check(
    queue: "Queue[UploadResult]",
    timeout: float | None,
    wip: List[str],
    output: Output | None = None,
) -> None:

    try:
        result = queue.get(block=(timeout is not None), timeout=timeout)
    except Empty:
        return

    wip.remove(result.key)

    pad = output.max_path if output else len(result.path)
    line = f"{result.path:<{pad}} ~> s3:/{result.bucket}/{result.key}"

    if result.exception:
        _logger.error(line, exc_info=result.exception)
        raise result.exception

    _logger.info(line)

    if output:
        output.out.write(line)
        output.out.write("\n")


def upload(
    dir: str | Path,
    bucket: str | None = None,
    concurrent_uploads: int = 8,
    out: IO[str] | None = None,
    read_only: bool = False,
    region: str | None = None,
    ssm_param: str | None = None,
) -> None:
    """
    Uploads the local directory `dir` to an S3 bucket.

    The bucket name must be set directly via `bucket` or read from the Systems
    Manager parameter named `ssm_param`.

    If `region` is not set then the default region will be used.

    `concurrent_uploads` describes the maximum number of concurrent upload
    threads to allow.

    `out` describes an optional string writer for progress reports. The same
    information will be available via logging, but this could be used for human-
    readable output (especially of read-only runs) at run-time. To write
    progress to the console, set to `sys.stdout`.

    If `read_only` is truthy then directories will be walked and files will be
    read, but nothing will be uploaded.
    """

    bucket = bucket_name(bucket, ssm_param, region)

    if isinstance(dir, str):
        dir = Path(dir)

    dir = dir.resolve().absolute()

    _logger.debug(
        "Starting %s concurrent %s of %s to %s in %s.",
        concurrent_uploads,
        "read-only uploads" if read_only else "uploads",
        dir,
        bucket,
        region,
    )

    files = Files(dir)
    output = Output(max_path=files.max_path, out=out) if out else None
    process_count = 0
    queue: "Queue[UploadResult]" = Queue(concurrent_uploads)
    wip: List[str] = []

    while True:
        full = len(wip) >= concurrent_uploads

        if wip:
            # If we *can* take on more work then don't wait; hurry up and add
            # more threads. Wait only when there's nothing more we can do.
            timeout = 1 if full else None
            check(output=output, queue=queue, timeout=timeout, wip=wip)

        if full:
            continue

        if file := files.next:

            wip.append(file.key)

            upload = Upload(
                bucket=bucket,
                cache_control=cache_control(file.path.relative_to(dir)),
                content_type=content_type(file.path.suffix),
                key=file.key,
                path=file.path.as_posix(),
                queue=queue,
                read_only=read_only,
                region=region,
            )

            upload.start()
            process_count += 1
            continue

        if not wip:
            _logger.debug("No files remaining. Upload complete.")
            return
