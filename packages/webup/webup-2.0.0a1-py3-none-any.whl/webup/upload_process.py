from multiprocessing import Process, Queue

from webup.models import UploadResult
from webup.session import make_session


class Upload(Process):
    def __init__(
        self,
        bucket: str,
        cache_control: str,
        content_type: str,
        key: str,
        path: str,
        queue: "Queue[UploadResult]",
        read_only: bool,
        region: str | None,
    ) -> None:

        super().__init__()

        self.bucket = bucket
        self.cache_control = cache_control
        self.content_type = content_type
        self.key = key
        self.path = path
        self.queue = queue
        self.read_only = read_only

        # Boto3 sessions are *not* threadsafe, so we intentionally pass in a
        # region to create our own session on-demand.
        self.region = region

    def run(self) -> None:
        result = UploadResult(
            bucket=self.bucket,
            path=self.path,
            key=self.key,
        )

        try:
            self.try_upload()
            self.queue.put(result)

        except Exception as ex:
            result.exception = ex
            self.queue.put(result)

    def try_upload(self) -> None:
        # Create the client even if we're running read-only to verify that our
        # credentials at least *seem* okay at first glance.
        #
        # pyright: reportUnknownMemberType=false
        s3 = make_session(self.region).client("s3")

        with open(self.path, "rb") as fp:
            if self.read_only:
                # Verify that we can read the file.
                fp.read()
                return

            s3.put_object(
                Body=fp,
                Bucket=self.bucket,
                CacheControl=self.cache_control,
                ContentType=self.content_type,
                Key=self.key,
            )
