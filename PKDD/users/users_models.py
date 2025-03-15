from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from sqlalchemy import Integer, String, ForeignKey, DateTime,\
    Numeric, Date, SmallInteger, select
from sqlalchemy.orm import Session
from flask_sqlalchemy.model import DefaultMeta
from PKDD import db
from authlib.jose import JsonWebToken
from datetime import timedelta, timezone        
from flask import current_app
from PKDD import login_manager
from flask_login import UserMixin


jwt_instance = JsonWebToken(['HS256'])


@login_manager.user_loader
def load_user(user_id):
    with Session(db.engines['users']) as session:
        return session.get(User, int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __bind_key__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    number_of_downloads: Mapped[int] = mapped_column(Integer, default=0)


    def get_token(self, expires_sec=1800):
        exp_timestamp = int((datetime.now(timezone.utc) + timedelta(seconds=expires_sec)).timestamp())
        secret = current_app.config['SECRET_KEY']
        header = {'alg': 'HS256'}
        payload = {'user_id': self.id, 'exp': exp_timestamp}
        token = jwt_instance.encode(header, payload, secret)
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token
    
    @staticmethod
    def verify_token(token):
        secret = current_app.config['SECRET_KEY']
        claims = jwt_instance.decode(token, secret)
        claims.validate()
        user_id = claims.get('user_id')
        if user_id is None:
            return None
        
        with Session(db.engines['users']) as session:
            return session.get(User, 'user_id') 
            
        
