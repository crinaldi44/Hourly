from flask import Flask, render_template
from models.employees.routes import employees
from auth.authentication import authentication
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.register_blueprint(employees)
app.register_blueprint(authentication)

# Represents the JWT secret key.
app.config['SECRET_KEY'] = 'c70665d063ec6aff812d5a58c2118e18'
app.config['PRODUCTION'] = False
app.config['DEV_DATABASE_URI'] = 'mysql+pymysql://root:test123@localhost:3306/employees'
app.config['PROD_DATABASE_URI'] = 'mysql+pymysql://admin:testing123456@database-1.cicovww9r07h.us-east-1.rds.amazonaws.com:3306/employees' # Update for production


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
