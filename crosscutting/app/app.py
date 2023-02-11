import os
from xml.dom import ValidationErr
import connexion
from openapi_server.encoder import JSONEncoder

from werkzeug.exceptions import UnprocessableEntity, InternalServerError, NotFound
from crosscutting.exception.error_handlers import handle_attribute_exception, handle_hourly_exception, handle_invalid_request, handle_marshmallow_validation_error, handle_notfound_exception, handle_unexpected_exception, handle_validation_error
from crosscutting.exception.hourly_exception import HourlyException
from sqlalchemy.exc import InvalidRequestError


class HourlyAPI(connexion.FlaskApp):
    """
    Wraps the main application in a general FlaskApp to handle general configuration of
    the API.
    """

    def __init__(self, specification_dir, **kwargs):
        """
        This initializes a new Connexion API class, generally to configure the application
        environment.
        """
        super().__init__(__name__, specification_dir=specification_dir, **kwargs)
        self.add_api('openapi.yaml', strict_validation=True, pythonic_params=True)
        self._configure()
        self._init_env()


    def _init_env(self):
        """
        Load dotenv variables into the application configuration environment.
        TODO: This should be an enum "Config" which hosts pre-configured vars for
        production and development.
        """
        self.app.config['SECRET_KEY'] = 'c70665d063ec6aff812d5a58c2118e18'
        self.app.config['PRODUCTION'] = False
        self.app.config['DEV_DATABASE_URI'] = 'postgresql://crinaldi:test123@0.0.0.0:5432/employees'
        self.app.config['PROD_DATABASE_URI'] = 'postgresql://chris:D41QYbmhlrjIXuQfJiQ4@hourly-postgres-prod.cicovww9r07h.us-east-1.rds.amazonaws.com:5432/employees'
        self.app.config['DEFAULT_JWT_EXPIRATION'] = {"hours": 2}
        self.app.config['DEFAULT_RATE_LIMIT'] = 100 # Measured in requests per minute
        self.app.config['CORS_HEADERS'] = 'X-Total-Count'

    def _configure(self):
        """
        Initializes configuration on the application. Registers error handlers, JSON model
        serialization encoders, and general configuration.
        """
        self.app.json_encoder = JSONEncoder
        self.app.register_error_handler(UnprocessableEntity, handle_validation_error)
        self.app.register_error_handler(AttributeError, handle_attribute_exception)
        self.app.register_error_handler(HourlyException, handle_hourly_exception)
        self.app.register_error_handler(InternalServerError, handle_unexpected_exception)
        self.app.register_error_handler(InvalidRequestError, handle_invalid_request)
        self.app.register_error_handler(NotFound, handle_notfound_exception)
        self.app.register_error_handler(ValidationErr, handle_marshmallow_validation_error)

