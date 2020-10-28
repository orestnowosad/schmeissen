from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

from config import ProductionConfig


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'login'
login.login_message = 'Log in to access this page.'
socketio = SocketIO(app)


def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # There's some weird shit with SQLite where this is necessary.
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_bath=True)
        else:
            migrate.init_app(app, db)

    login.init_app(app)
    socketio.init_app(app)

    return app
