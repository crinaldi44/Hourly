import os
from xml.dom import ValidationErr
import connexion
from flask_cors import CORS

from crosscutting.core.config import config
from openapi_server.encoder import JSONEncoder

from werkzeug.exceptions import UnprocessableEntity, InternalServerError, NotFound
from crosscutting.exception.error_handlers import handle_attribute_exception, handle_hourly_exception, \
    handle_invalid_request, handle_marshmallow_validation_error, handle_notfound_exception, handle_unexpected_exception, \
    handle_validation_error
from crosscutting.exception.hourly_exception import HourlyException
from sqlalchemy.exc import InvalidRequestError
import uuid


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
        super().__init__(__name__, specification_dir=os.path.abspath(specification_dir), **kwargs)
        self.add_api('openapi.yaml', strict_validation=True, validate_responses=True, pythonic_params=True)
        self._configure()
        self._init_env()

    def _init_env(self):
        """
        Load environment variables into the application configuration environment. These
        can be specified with APP_ENV=dev or APP_ENV=prod.
        """
        self.app.config.from_object("crosscutting.core.config.config.flask_config")
        self.app.config['SECRET_KEY'] = str(uuid.uuid4())
        self.app.config['CORS_HEADERS'] = config.config.CORS_HEADERS

    def _configure(self):
        """
        Initializes configuration on the application. Registers error handlers, JSON model
        serialization encoders, and CORS policy.
        """
        self.app.json_encoder = JSONEncoder
        self.app.register_error_handler(UnprocessableEntity, handle_validation_error)
        self.app.register_error_handler(AttributeError, handle_attribute_exception)
        self.app.register_error_handler(HourlyException, handle_hourly_exception)
        self.app.register_error_handler(InternalServerError, handle_unexpected_exception)
        self.app.register_error_handler(InvalidRequestError, handle_invalid_request)
        self.app.register_error_handler(NotFound, handle_notfound_exception)
        self.app.register_error_handler(ValidationErr, handle_marshmallow_validation_error)
        CORS(app=self.app, expose_headers=['X-Total-Count'])
