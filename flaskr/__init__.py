import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        SQLALCHEMY_DATABASE_URI=os.getenv(
            'DATABASE_URL',
            'postgresql://flaskuser:flaskpass@localhost:5432/flaskr'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    app.config.from_mapping(
        SMTP_SERVER=os.environ.get("SMTP_SERVER"),
        SMTP_PORT=int(os.environ.get("SMTP_PORT", 465)),
        SMTP_USERNAME=os.environ.get("SMTP_USERNAME"),
        SMTP_PASSWORD=os.environ.get("SMTP_PASSWORD"),

        TWILIO_ACCOUNT_SID=os.environ.get("TWILIO_ACCOUNT_SID"),
        TWILIO_AUTH_TOKEN=os.environ.get("TWILIO_AUTH_TOKEN"),
        TWILIO_PHONE_NUMBER=os.environ.get("TWILIO_PHONE_NUMBER"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    from . import auth
    app.register_blueprint(auth.bp)

    from . import goals
    app.register_blueprint(goals.bp)
    app.add_url_rule('/', endpoint='index')

    from . import test_routes
    app.register_blueprint(test_routes.bp)

    migrate.init_app(app, db)

    return app
