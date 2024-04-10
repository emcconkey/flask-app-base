from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from logging.config import dictConfig

if os.environ.get('RUN_MODE'):
    load_dotenv(f"env/env.{os.environ.get('RUN_MODE')}")
else:
    load_dotenv("env/env.production")

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(module)s %(message)s',
    }},
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': os.environ.get('LOGFILE'),
            'formatter': 'default',
            'level': 'ERROR'
        }
    },
    'root': {
        'level': 'ERROR',
        'handlers': ['file']
    }
})

application = Flask(__name__)

application.config['SECRET_KEY'] = os.environ.get('APP_SECRET_KEY')

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}'.format(
    os.environ.get('DB_USER'),
    os.environ.get('DB_PASSWORD'),
    os.environ.get('DB_HOST'),
    os.environ.get('DB_DATABASE')
)

if os.environ.get('SENTRY_ENDPOINT'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_ENDPOINT'),
        integrations=[FlaskIntegration()],
        environment=os.environ.get('RUN_MODE'),
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production.
        traces_sample_rate=1.0
    )

application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(application)
sql_migrate = Migrate(application, database)
login_manager = LoginManager(application)


def db():
    return database


def app():
    return application


def migrate():
    return sql_migrate


def login():
    return login_manager
