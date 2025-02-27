from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from PKDD.config import Config

# app = Flask(__name__)
# app.config.from_object(Config)
db = SQLAlchemy()

from PKDD.financial_db.financial_models import Model, Disposition, Account, Trans, Loan, Order, Client,\
    District, Card


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        from PKDD.dash_page.dash_charts import charts
    app.register_blueprint(charts)
    return app
