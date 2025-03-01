from PKDD import db, create_app
from PKDD.config import Config 
from flask import current_app, Flask
from typing import List
from PKDD.financial_db.financial_models import Model, Disposition, Account, Trans, Loan, Order, Client,\
    District, Card
from pandas import DataFrame
from PKDD.financial_db.data_mainpualtion import RepairData, FinancialDataBase
from typing import List
import zipfile


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():

        tables: List[[Model]] = [District, Account, Trans, Loan, Order, Client,  Disposition, Card ]
        csvs: List[str] = ['csv/district.asc', 'csv/account.asc', 'csv/trans.asc', 'csv/loan.asc',\
                'csv/order.asc', 'csv/client.asc', 'csv/disp.asc', 'csv/card.asc']
        data_obj = RepairData(csvs, tables)
        data: dict[Model:DataFrame] = data_obj.load_data()
        # financial_db = FinancialDataBase(data)
    for table, df in data.items():
        df.to_csv('PKDD/static/cleaned_csvs/'+ table.__tablename__+'.csv', index=False)

    with zipfile.ZipFile('PKDD/static/cleaned_csvs/cleaned_csvs.zip', 'w') as zipf:
        for table, df in data.items():
            zipf.write('PKDD/static/cleaned_csvs/'+ table.__tablename__+'.csv')
        