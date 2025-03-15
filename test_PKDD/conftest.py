import pytest
from PKDD import create_app, db
import os
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import warnings
from PKDD.users.users_models import User


class TestConfig:
    load_dotenv()
    '''Konfiguracja dla testów.'''
    SECRET_KEY = 'test_secret'
    SQLALCHEMY_BINDS = {'users': 'sqlite:///:memory:',
                        'statistics': os.getenv('SQLALCHEMY_FINANCIAL_DATABASE_URI')} 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'localhost'  
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = None
    SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    RECAPTCHA_KEY = os.getenv('RECAPTCHA_KEY')
    RECAPTCHA_VERIFY_URL = os.getenv('RECAPTCHA_VERIFY_URL')
    UPLOAD_DIRECTORY = 'static/cleaned_csvs'

@pytest.fixture
def app():
    warnings.filterwarnings("ignore", category=DeprecationWarning, module="_plotly_utils.basevalidators")

    '''Tworzy instancję aplikacji Flask z konfiguracją testową.'''
    app = create_app(config_class=TestConfig) 
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Wyłącz CSRF na potrzeby testów
    app.config['LOGIN_DISABLED'] = True  
    app.config['SERVER_NAME'] = 'localhost'

    with app.app_context():
        yield app  
        
@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all(bind_key='users') 
        yield db
        db.drop_all(bind_key='users')  

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    '''Zwraca testowego CLI runnera dla komend Flask.'''
    return app.test_cli_runner()
