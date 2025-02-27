from PKDD import db, app
from typing import List
from PKDD.financial_db.financial_models import Model, Disposition, Account, Trans, Loan, Order, Client,\
    District, Card
from pandas import DataFrame
from PKDD.financial_db.create_db import RepairData, FinancialDataBase
from typing import List

if __name__ == '__main__':
    with app.app_context():

        tables: List[[Model]] = [District, Account, Trans, Loan, Order, Client,  Disposition, Card ]
        csvs: List[str] = ['csv/district.asc', 'csv/account.asc', 'csv/trans.asc', 'csv/loan.asc',\
                'csv/order.asc', 'csv/client.asc', 'csv/disp.asc', 'csv/card.asc']
        data_obj = RepairData(csvs, tables)
        data: dict[Model:DataFrame] = data_obj.load_data()
        # financial_db = FinancialDataBase(data)
    for table, df in data.items():
        df.to_csv('PKDD/cleaned_csvs/'+ table.__tablename__+'.csv', index=False)

        