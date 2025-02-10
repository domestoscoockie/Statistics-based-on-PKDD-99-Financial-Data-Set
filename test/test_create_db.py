import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session, DeclarativeBase
from creeate_db import _Base, Trans, Loan, Order, Account,\
Card, Disposition, Client, District

class Db_creation:

    def setup_class(self):
        _Base.metadata  



