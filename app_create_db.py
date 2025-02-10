from connection import Connection_to_db
import numpy as np
from time import time
from creeate_db import Account, Trans, Loan, Order,Card, Disposition, Client,\
    District, _Base
from sqlalchemy.orm import Session
import pandas as pd
from typing import List



class FinancialDataBase():
    ''' Using csv files and Sqlalchemy ORM tables inserts data from files to data base. Here are also few methods to repair data   
    '''
    def __init__(self, csvs: List[str], tables: List['_Base']):
        self.engine = Connection_to_db().engine
        self.csvs = csvs
        self.tables = tables
        with Session(self.engine) as self.session:
            self.upload_data(self.load_data())
            self.session.commit()

    def load_data(self) -> dict[pd.DataFrame]:
        data_frames = {}

        for file, table in zip(self.csvs, self.tables): #files and tables names
            self.columns = [col.name for col in table.__table__.columns]
            self.df = pd.read_csv(file, sep=';', names=self.columns, low_memory=False, header=0)
            self.df = self.df = self.wrong_values_to_none()
            if table == Account or table == Card:
                self.df = self.str_date_to_date_type(file)
            elif table in (District, Order, Trans):
                self.convert_to_right_type(['unemployment_rate_95','crimes_95'],['float', 'integer']) if table == District else None
                self.convert_to_right_type(['account'],['integer']) if table == Trans else None 
            data_frames[table] = self.df
            

        return data_frames


    def upload_data(self, data_frames:dict['_Base':pd.DataFrame]) -> None:
            for table, df in data_frames.items():
                records = df.to_dict(orient='records')
                self.session.bulk_insert_mappings(table,records)


    def convert_to_right_type(self, columns: list[str], types: list[str]) -> None:

        for col, col_type in zip(columns,types):
            if col_type == 'integer':
                self.df[col] = pd.to_numeric(self.df[col],errors='coerce',downcast=col_type).round().astype('Int64')
            elif col_type =='float':
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce', downcast=col_type)
            self.df[col] = self.df[col].replace({'?':None, np.nan:None,'<Na>':None, 'Nan': None, pd.NA: None, 'nan': None, '':None, ' ':None})


    def wrong_values_to_none(self) -> None:
        self.df = self.df.replace({'?':None, '<Na>':None, pd.NA: None,'nan': None, '':None, ' ':None})
        return self.df
    
    def analyze_date_format(self, date_str: int) -> pd.DataFrame:
        date_str = str(date_str)
        date_str = date_str.split(' ')[0] if ' ' in date_str else date_str
        df = pd.to_datetime(date_str, format='%y%m%d', errors='coerce')
        df = df.strftime('%Y-%m-%d')
        return df
    
        
    def str_date_to_date_type(self, file: str) -> pd.DataFrame:
        column = 'date' if file == 'csv/account.asc' else 'issued'
        self.df[column] = self.df[column].apply(self.analyze_date_format)
        return self.df
    

    def __repr__(self):
        return 'FinancialDataBase()'

if __name__ == '__main__':
    connection = Connection_to_db()
    t = time()
    _Base.metadata.create_all(connection.engine)    
    tables: List['_Base'] = [District, Account, Trans, Loan, Order, Client,  Disposition, Card ]
    csvs: List[str] = ['csv/district.asc', 'csv/account.asc', 'csv/trans.asc', 'csv/loan.asc',\
            'csv/order.asc', 'csv/client.asc', 'csv/disp.asc', 'csv/card.asc']
    app = FinancialDataBase(csvs, tables)
    print(time()-t)
    