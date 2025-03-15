from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
import datetime 
from sqlalchemy import Integer, String, ForeignKey, DateTime,\
    Numeric, Date, SmallInteger
from flask_sqlalchemy.model import DefaultMeta
from PKDD import db


class Trans(db.Model):
    __tablename__ = 'trans'
    __bind_key__ = 'statistics'

    trans_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(Integer,ForeignKey('account.account_id'))
    date: Mapped[datetime.date] = mapped_column(Date)
    transaction_type: Mapped[str] = mapped_column(String(30))
    operation: Mapped[str] = mapped_column(String(30), nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(10,2))
    ballance: Mapped[float] = mapped_column(Numeric(10,2))
    k_symbol: Mapped[str] = mapped_column(String(30),nullable=True)
    bank: Mapped[str] = mapped_column(String(5), nullable=True)
    account: Mapped[int] = mapped_column(Integer, nullable=True)

    account_relation: Mapped['Account'] = relationship('Account', back_populates='trans')


class Loan(db.Model):
    __tablename__ = 'loan'
    __bind_key__ = 'statistics'
    
    loan_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    account_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('account.account_id'))
    date: Mapped[datetime.date] = mapped_column(Date)
    amount: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(SmallInteger)
    payments: Mapped[float] = mapped_column(Numeric(10,2))
    status: Mapped[str] = mapped_column(String(35))

    account_relation: Mapped['Account'] = relationship('Account',back_populates='loan')


class Order(db.Model):
    __tablename__ = 'order'
    __bind_key__ = 'statistics'

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('account.account_id'))
    bank_to: Mapped[str] = mapped_column(String(2))
    account_to: Mapped[int] = mapped_column(Integer)
    amount: Mapped[float] = mapped_column(Numeric(10,2))
    k_symbol: Mapped[str] = mapped_column(String(18), nullable=True)

    account_relation: Mapped['Account'] = relationship('Account', back_populates='order')


class Account(db.Model):
    __tablename__ = 'account'
    __bind_key__ = 'statistics'
    
    account_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    district_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('district.district_id'))
    frequency: Mapped[str] = mapped_column(String(30))
    date: Mapped[datetime.date] = mapped_column(Date)

    trans: Mapped['Trans'] = relationship('Trans', back_populates='account_relation')
    loan: Mapped['Loan'] = relationship('Loan', back_populates='account_relation')
    order: Mapped['Order'] = relationship('Order', back_populates='account_relation')
    disposition: Mapped['Disposition'] = relationship('Disposition', back_populates='account_relation')
    district: Mapped['District'] = relationship('District', back_populates='account_relation')


class Card(db.Model):
    __tablename__ = 'card'
    __bind_key__ = 'statistics'

    card_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    disposition_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('disposition.disposition_id'))
    type: Mapped[str] = mapped_column(String(10))
    issued: Mapped[DateTime] = mapped_column(Date)
    
    disposition:Mapped['Disposition'] = relationship('Disposition', back_populates='card')


class Disposition(db.Model):
    __tablename__ = 'disposition'
    __bind_key__ = 'statistics'

    disposition_id: Mapped[int] = mapped_column(SmallInteger, primary_key=True)
    client_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('client.client_id'))
    account_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('account.account_id'))
    type: Mapped[str] = mapped_column(String(10))
    
    account_relation: Mapped['Account'] = relationship('Account', back_populates='disposition') 
    client: Mapped['Client'] = relationship('Client', back_populates='disposition')
    card: Mapped['Card'] = relationship('Card', back_populates='disposition')


class Client(db.Model):
    __tablename__ = 'client'
    __bind_key__ = 'statistics'
    
    client_id: Mapped[int] = mapped_column(SmallInteger,primary_key=True)
    birth_number: Mapped[str] = mapped_column(String(6))
    district_id: Mapped[int] = mapped_column(SmallInteger, ForeignKey('district.district_id'))

    disposition: Mapped['Disposition'] = relationship('Disposition', back_populates='client')
    district: Mapped['District'] = relationship('District', back_populates='client')



class District(db.Model):
    __tablename__ = 'district'
    __bind_key__ = 'statistics'

    district_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    district_name: Mapped[str] = mapped_column(String(30))
    region: Mapped[str] = mapped_column(String(30))
    num_inhabitants: Mapped[int] = mapped_column(Integer)  # A4
    num_municipalities_lt_499: Mapped[int] = mapped_column(SmallInteger)  # A5
    num_municipalities_500_1999: Mapped[int] = mapped_column(SmallInteger)  # A6
    num_municipalities_2000_9999: Mapped[int] = mapped_column(SmallInteger)  # A7
    num_municipalities_gt_10000: Mapped[int] = mapped_column(SmallInteger)  # A8
    num_cities: Mapped[int] = mapped_column(SmallInteger)  # A9
    urban_inhabitant_ratio: Mapped[float] = mapped_column(Numeric(8, 2))  # A10
    avg_salary: Mapped[int] = mapped_column(Integer)  # A11
    unemployment_rate_95: Mapped[float] = mapped_column(Numeric(5, 2), nullable=True)  # A12
    unemployment_rate_96: Mapped[float] = mapped_column(Numeric(5, 2))  # A13
    entrepreneurs_per_1000: Mapped[int] = mapped_column(Integer)  # A14
    crimes_95: Mapped[int] = mapped_column(Integer, nullable=True)  # A15
    crimes_96: Mapped[int] = mapped_column(Integer)  # A16


    client: Mapped['Client'] = relationship('Client', back_populates='district')
    account_relation: Mapped['Account'] = relationship('Account', back_populates='district')


