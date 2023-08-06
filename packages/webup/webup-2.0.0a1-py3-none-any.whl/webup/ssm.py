from boto3.session import Session


def get_ssm_value(param: str, session: Session) -> str:
    ssm = session.client("ssm")  # pyright: reportUnknownMemberType=false
    try:
        return ssm.get_parameter(Name=param)["Parameter"]["Value"]
    except KeyError:
        raise
