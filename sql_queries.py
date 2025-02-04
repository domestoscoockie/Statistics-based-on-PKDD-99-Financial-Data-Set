from connection import Connection_to_db
from creeate_db import _Base, Client, Account, Card, District, Disposition, Loan, Order, Trans
from sqlalchemy.orm import Session
from sqlalchemy import select, func 
import pandas as pd


class CreditScore(Connection_to_db):

    def score_by_region(self, region_name: str):
        with Session(self.engine) as session:
            result = session.execute(
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

    def number_of_trans_per_account(self):
        with Session(self.engine) as session:
            result = session.execute(
                select(
                    Trans.account_id,
                    func.count(Trans.trans_id).label('trans_count')
                    )
                    .group_by(Trans.account_id)
                )

            return result

class CursorAsDataFrame(CreditScore):

    def score_by_region(self, region_name: str):
        cursor =  super().score_by_region(region_name)
        return pd.DataFrame(cursor.fetchall(), columns=cursor.keys())


    def number_of_trans_per_account(self):
        cursor = super().number_of_trans_per_account()
        return pd.DataFrame(cursor.fetchall(), columns=cursor.keys())


if __name__ == '__main__':
    x = CursorAsDataFrame()
    print(x.score_by_region('Prague')
    )    
