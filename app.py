from flask import Flask, render_template
from models.employees.routes import employees
from auth.authentication import authentication

app = Flask(__name__)

app.config['SECRET_KEY'] = 'c70665d063ec6aff812d5a58c2118e18'
app.register_blueprint(employees)
app.register_blueprint(authentication)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/dashboard')
def present_dashboard():
    return render_template('dashboard.html')


if __name__ == '__main__':
    app.run()
