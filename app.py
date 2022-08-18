import sqlalchemy.exc
from flask import Flask, render_template
from marshmallow import ValidationError

from domains.employees.routes.routes import employees
from domains.roles.routes.routes import roles
from domains.departments.routes.routes import departments
from domains.clockins.routes.routes import clockins
from domains.packages.routes.routes import packages
from domains.companies.routes.routes import companies
from flask_cors import CORS
from werkzeug.exceptions import UnprocessableEntity, InternalServerError, NotFound
from crosscutting.exception.error_handlers import handle_hourly_exception, handle_validation_error, handle_unexpected_exception, handle_attribute_exception, handle_marshmallow_validation_error, handle_invalid_request, handle_notfound_exception
import crosscutting.exception.hourly_exception
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

app.register_blueprint(employees)
app.register_blueprint(roles)
app.register_blueprint(departments)
app.register_blueprint(clockins)
app.register_blueprint(packages)
app.register_blueprint(companies)

app.register_error_handler(UnprocessableEntity, handle_validation_error)
app.register_error_handler(AttributeError, handle_attribute_exception)
app.register_error_handler(crosscutting.exception.hourly_exception.HourlyException, handle_hourly_exception)
app.register_error_handler(InternalServerError, handle_unexpected_exception)
app.register_error_handler(sqlalchemy.exc.InvalidRequestError, handle_invalid_request)
app.register_error_handler(NotFound, handle_notfound_exception)
app.register_error_handler(ValidationError, handle_marshmallow_validation_error)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['150 per minute']
)

CORS(app=app, expose_headers=['X-Total-Count'])

# Represents the JWT secret key.
app.config['SECRET_KEY'] = 'c70665d063ec6aff812d5a58c2118e18'
app.config['PRODUCTION'] = False
app.config['DEV_DATABASE_URI'] = 'mysql+pymysql://root:test123@localhost:3306/employees'
app.config['PROD_DATABASE_URI'] = 'mysql+pymysql://admin:testing123456@database-1.cicovww9r07h.us-east-1.rds.amazonaws.com:3306/employees' # Update for production
app.config['DEFAULT_JWT_EXPIRATION'] = {"hours": 2}
app.config['DEFAULT_RATE_LIMIT'] = 100 # Measured in requests per minute
app.config['CORS_HEADERS'] = 'X-Total-Count'


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bind_address = '0.0.0.0:' + str(port)
    app.run(host=bind_address)
