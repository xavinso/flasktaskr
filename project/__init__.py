import datetime
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_pyfile('_config.py')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.tasks.views import tasks_blueprint
from project.api.views import api_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)


def log_error(code, url):
    print app.debug
    if app.debug is not True:
        now = datetime.datetime.now()
        with open('error.log', 'a') as f:
            current_timestamp = now.strftime("%d-%m-%Y %H:%M:%S")
            f.write("\n{} error at {}: {}".format(
                code, current_timestamp, url))


@app.errorhandler(404)
def not_found(error):
    log_error(404, request.url)
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    log_error(500, request.url)
    return render_template('500.html'), 500
