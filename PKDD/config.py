import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_FINANCIAL_DATABASE_URI')
    SQLALCHEMY_BINDS = {'users' : os.getenv('SQLALCHEMY_USERS_DATABASE_URI')}
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')
    SITE_KEY = os.getenv('RECAPTCHA_SITE_KEY')
    RECAPTCHA_KEY = os.getenv('RECAPTCHA_KEY')
    RECAPTCHA_VERIFY_URL = os.getenv('RECAPTCHA_VERIFY_URL')