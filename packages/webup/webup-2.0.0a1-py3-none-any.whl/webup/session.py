from boto3.session import Session


def make_session(region: str | None = None) -> Session:
    return Session(region_name=region) if region else Session()
