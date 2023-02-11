import base64
import enum
import os
import uuid
from copy import deepcopy
from types import SimpleNamespace


class Config(object):
    """
    This loads application-critical variables from the application environment. Critical vars such as
    secrets have a fallback, but should be generated prior to running the app.
    """
    PORT = int(os.getenv("PORT", 8080))
    JWT_ACCESS_PUBLIC_KEY_SECRET_ENCODED = os.getenv("JWT_ACCESS_PUBLIC_KEY_SECRET_ENCODED", "")
    JWT_ACCESS_PUBLIC_KEY_SECRET = base64.b64decode(JWT_ACCESS_PUBLIC_KEY_SECRET_ENCODED).decode("utf-8")

    JWT_SECRET_RANDOMIZED = "5ea1ae40-bd19-46ab-a817-97661710ac32"

    DEFAULT_RATE_LIMIT = None
    CORS_HEADERS = 'X-Total-Count'
    DEFAULT_JWT_EXPIRATION = {'hours': 2}

    JWT_ACCESS_PRIVATE_KEY_SECRET_ENCODED = os.getenv("JWT_ACCESS_PRIVATE_KEY_SECRET_ENCODED", "")
    JWT_ACCESS_PRIVATE_KEY_SECRET = base64.b64decode(JWT_ACCESS_PRIVATE_KEY_SECRET_ENCODED).decode("utf-8")

    POSTGRES_URI_ENCODED = os.getenv("POSTGRES_URI_ENCODED",
                                     "cG9zdGdyZXNxbDovL2NyaW5hbGRpOnRlc3QxMjNAMC4wLjAuMDo1NDMyL2VtcGxveWVlcw==")
    POSTGRES_URI = base64.b64decode(POSTGRES_URI_ENCODED).decode("utf-8")

    FLASK_CONFIG = SimpleNamespace()
    FLASK_CONFIG.ENV = 'development'


class ProductionConfig(Config):
    MODE = "prod"
    DEFAULT_RATE_LIMIT = 100

    FLASK_CONFIG = deepcopy(Config.FLASK_CONFIG)
    FLASK_CONFIG.ENV = "production"


class DevConfig(Config):
    MODE = "dev"
    FLASK_DEBUG = True

    FLASK_CONFIG = deepcopy(Config.FLASK_CONFIG)
    FLASK_CONFIG.ENV = "development"


ENVIRONMENT = os.getenv("APP_ENV", 'dev')
if ENVIRONMENT != "dev" and ENVIRONMENT != "prod":
    raise ValueError("Invalid environment mode APP_ENV")
config = ProductionConfig() if ENVIRONMENT == "prod" else DevConfig()
flask_config = config.FLASK_CONFIG

__all__ = ["config", "flask_config"]
