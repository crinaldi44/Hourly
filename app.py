import sqlalchemy.exc
from flask import Flask, render_template
from domains.employees.routes.routes import employees
from domains.roles.routes.routes import roles
from domains.departments.routes.routes import departments
from domains.clockins.routes.routes import clockins
from domains.packages.routes.routes import packages
from flask_cors import CORS
from werkzeug.exceptions import UnprocessableEntity, InternalServerError
from crosscutting.exception.error_handlers import handle_hourly_exception, handle_validation_error, handle_unexpected_exception, handle_attribute_exception, handle_invalid_request
import crosscutting.exception.hourly_exception

app = Flask(__name__)

CORS(app)

app.register_blueprint(employees)
app.register_blueprint(roles)
app.register_blueprint(departments)
app.register_blueprint(clockins)
app.register_blueprint(packages)

app.register_error_handler(UnprocessableEntity, handle_validation_error)
app.register_error_handler(AttributeError, handle_attribute_exception)
app.register_error_handler(crosscutting.exception.hourly_exception.HourlyException, handle_hourly_exception)
app.register_error_handler(InternalServerError, handle_unexpected_exception)
app.register_error_handler(sqlalchemy.exc.InvalidRequestError, handle_invalid_request)

# Represents the JWT secret key.
app.config['SECRET_KEY'] = 'c70665d063ec6aff812d5a58c2118e18'
app.config['PRODUCTION'] = False
app.config['DEV_DATABASE_URI'] = 'mysql+pymysql://root:test123@localhost:3306/employees'
app.config['PROD_DATABASE_URI'] = 'mysql+pymysql://admin:testing123456@database-1.cicovww9r07h.us-east-1.rds.amazonaws.com:3306/employees' # Update for production
app.config['DEFAULT_JWT_EXPIRATION'] = {"hours": 2}
app.config['CORS_HEADERS'] = 'X-Total-Count'

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/dashboard')
def present_dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    bind_address = '0.0.0.0:' + str(port)
    app.run(host=bind_address)
