import json
import logging
import boto3
import botocore.session

from aws_secretsmanager_caching import SecretCache, SecretCacheConfig

LOGGER = logging.getLogger(__name__)


def aws_config(secret_name: str) -> dict:
    """
    This function returns the secrets needed for the application from AWS
    Secrets Manager. We use caching because it is faster and will reduce costs.
    `aws_ssm_get_secrets`
    See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    """
    try:
        client = botocore.session.get_session().create_client("secretsmanager")
        cache_config = SecretCacheConfig()
        cache = SecretCache(config=cache_config, client=client)
        secrets = cache.get_secret_string(secret_name)
        return json.loads(secrets)
    except json.decoder.JSONDecodeError as ex:
        LOGGER.exception(f"aws_config: error decoding JSON: {ex}")
        raise ValueError("aws_config: invalid JSON in secret.")
    except Exception as ex:
        LOGGER.exception(f"aws_config: exception raised: {ex}")
        raise PermissionError("aws_config: permission denied.")


def aws_session(credentials: dict = None) -> boto3.Session:
    """
    This function is used to create an AWS Session object. If no service
    dictionary (and related credentials) are provided, then the local
    configuration i.e.: `.config` will be used.
    """
    try:
        session = boto3.Session(region_name="eu-west-1")
        if credentials:
            session.__init__(
                aws_access_key_id=credentials.get("aws_access_key_id"),
                aws_secret_access_key=credentials.get("aws_secret_access_key")
            )
        return session
    except (KeyError, Exception):
        LOGGER.exception("aws_session")


def aws_client(service_name: str, credentials: dict = None) -> boto3.Session.client:
    """
    This function is used to create an AWS Client object. The service
    (and related credentials) must be provided.
    """
    # First create the session object.
    session = aws_session(credentials=credentials)
    try:
        return session.client(service_name=service_name)
    except (KeyError, Exception):
        LOGGER.exception("aws_client")


def aws_resource(service_name: str, credentials: dict = None) -> boto3.Session.resource:
    """
    This function is used to create an AWS Resource object. The service
    (and related credentials) must be provided.
    """
    # First create the session object.
    session = aws_session(credentials=credentials)
    try:
        return session.resource(service_name=service_name)
    except (KeyError, Exception):
        LOGGER.exception("aws_resource")
