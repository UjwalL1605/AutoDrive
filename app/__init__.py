import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'routes.login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from . import routes, models
        app.register_blueprint(routes.bp)

    return app