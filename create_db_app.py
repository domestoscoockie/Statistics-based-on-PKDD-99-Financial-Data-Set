from PKDD import db, create_app
from PKDD.config import Config 
from flask import current_app, Flask
from typing import List
from PKDD.financial_db.financial_models import Disposition, Account, Trans, Loan, Order, Client,\
    District, Card
from pandas import DataFrame
from PKDD.financial_db.data_manipulation import RepairData, FinancialDataBase
import zipfile
from PKDD.users.users_models import User
import pg8000
from time import time
import sqlalchemy.exc

def cleaned_csv_files_creation(data):
    for table, df in data.items():
        df.to_csv('PKDD/static/cleaned_csvs/'+ table.__tablename__+'.csv', index=False)

    with zipfile.ZipFile('PKDD/static/cleaned_csvs/cleaned_csvs.zip', 'w') as zipf:
        for table, df in data.items():
            zipf.write('PKDD/static/cleaned_csvs/'+ table.__tablename__+'.csv')

if __name__ == '__main__':
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)
        t = time()
        with app.app_context():

            db.create_all(bind_key='statistics')
            
            tables = [District, Account, Trans, Loan, Order, Client,  Disposition, Card ]
            csvs: List[str] = ['csv/district.asc', 'csv/account.asc', 'csv/trans.asc', 'csv/loan.asc',\
                    'csv/order.asc', 'csv/client.asc', 'csv/disp.asc', 'csv/card.asc']  
            for table, csv in zip(tables, csvs):
                data_obj = RepairData([csv], [table])
                data = data_obj.load_data()
                FinancialDataBase(data)
            db.create_all(bind_key='users')
            print(time()-t)
    except sqlalchemy.exc.IntegrityError:
        print('Database already created')