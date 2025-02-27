from trash.connection import Connection_to_db
from PKDD.financial_db.financial_models import Client, Account, Card, District,\
    Disposition, Loan, Order, Trans
from sqlalchemy.orm import Session
from sqlalchemy import select, func, extract
import pandas as pd
from PKDD import db


class CreditScore:
    def __init__(self, session):
        self.session = session
    def score_by_region(self, region_name: str):
            result = self.session.execute(
                select(
                    func.count(Loan.amount).label("loan_count"),
                    Loan.status
                )
                .select_from(Loan)
                .join(Account, Loan.account_id == Account.account_id)
                .join(District, District.district_id == Account.district_id)
                .where(District.region == region_name)
                .group_by(Loan.status, District.region)
            )

            return result

    def number_of_trans_by_region(self):
            result = self.session.execute(
                select(District.region,
                    func.count(Trans.trans_id).label("count")
                    )
                    .join(Account, Account.account_id == Trans.account_id)
                    .join(District, District.district_id == Account.district_id)
                    .group_by(District.region)
                    .order_by('count')
                )

            return result


    def number_of_tarns_per_month(self, year: str):
        
            result = self.session.execute(
            select(
                extract('month', Trans.date).label('month'),
                extract('year', Trans.date).label('year'),
                func.count(Trans.trans_id).label('count')
            )
            .where(extract('year', Trans.date) == int(year))
            .group_by(extract('year', Trans.date), extract('month', Trans.date))
            .order_by(extract('year', Trans.date), extract('month', Trans.date))
            )
            return result

    def __repr__(self):
        return 'CreditScore()'

class CursorAsDataFrame(CreditScore):

    def score_by_region(self, region_name: str):
        cursor =  super().score_by_region(region_name)
        return pd.DataFrame(cursor.fetchall(), columns=cursor.keys())


    def number_of_trans_by_region(self):
        cursor = super().number_of_trans_by_region()
        return pd.DataFrame(cursor.fetchall(), columns=cursor.keys())

    def number_of_tarns_per_month(self, year: str):    
        cursor = super().number_of_tarns_per_month(year)
        return pd.DataFrame(cursor.fetchall(), columns=cursor.keys())

    def __repr__(self):
        return 'CursorAsDataFrame()'

if __name__ == '__main__':
    x = CursorAsDataFrame()
    print(x.number_of_tarns_per_month(1999)
    )    
