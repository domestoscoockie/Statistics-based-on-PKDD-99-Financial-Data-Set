import numpy as np
from time import time
from PKDD.financial_db.financial_models import Account, Trans, Loan, Order,Card, Disposition, Client,\
    District
from sqlalchemy.orm import Session
import pandas as pd
from typing import List, Type, Dict
from PKDD import db
from PKDD.financial_db.wrong_values import column_specific_replacements, global_replacements

pd.set_option('future.no_silent_downcasting', True) #data types shouldn't be changed by pandas without concent 


class RepairData:
    _DATE_FORMATS = {
        'account.asc': ('date', '%y%m%d'),
        'card.asc': ('issued', '%y%m%d %H:%M:%S')
    }

    _SPECIAL_NUMERIC_HANDLING = {
        Trans: ['account']
    }

    def __init__(self, csvs: List[str], tables: List[Type[db.Model]]) -> None:
        self.csvs = csvs
        self.tables = tables
        self._dtype_cache = {}

    def _get_dtype_mapping(self, table: Type[db.Model]) -> Dict[str, str]:
        #Handling data types changes
        if table not in self._dtype_cache:
            mapping = {}
            for col in table.__table__.columns:
                py_type = col.type.python_type
                if py_type == int:
                    mapping[col.name] = 'Int32'
                elif py_type == float:
                    mapping[col.name] = 'float32'
                elif py_type == str and col.name in column_specific_replacements.get(table.__name__, {}):
                    mapping[col.name] = 'category'
                else:
                    mapping[col.name] = 'object'
            self._dtype_cache[table] = mapping
        return self._dtype_cache[table]

    def _process_chunk(self, chunk: pd.DataFrame, table: Type[db.Model], file: str) -> pd.DataFrame:
        # Replacing Czech names and values written as A,B,C etc. 
        table_name = table.__name__
        if table_name in column_specific_replacements:
            for col, mapping in column_specific_replacements[table_name].items():
                if col in chunk.columns:
                    chunk[col] = chunk[col].replace(mapping).astype('category')

        #Replacing numbers written as strings 
        if table in self._SPECIAL_NUMERIC_HANDLING:
            for col in self._SPECIAL_NUMERIC_HANDLING[table]:
                if col in chunk.columns:
                    chunk[col] = pd.to_numeric(chunk[col], errors='coerce', downcast='integer')

        # Date conversion
        if file in self._DATE_FORMATS:
            col_name, date_format = self._DATE_FORMATS[file]
            chunk[col_name] = pd.to_datetime(chunk[col_name], format=date_format, errors='coerce')

        # Removing weird non data 
        chunk = chunk.replace(global_replacements)
        numeric_cols = chunk.select_dtypes(include=np.number).columns
        chunk[numeric_cols] = chunk[numeric_cols].replace({'?': np.nan, '': np.nan, ' ': np.nan})
        
        return chunk

    def load_data(self) -> Dict[Type[db.Model], pd.DataFrame]:
        data_frames = {}

        for file, table in zip(self.csvs, self.tables):
            chunks = []
            dtype_mapping = self._get_dtype_mapping(table)
            columns = [col.name for col in table.__table__.columns]

            #loading data as chunks to not overload server 
            for chunk in pd.read_csv(file, sep=';', names=columns, dtype=dtype_mapping, low_memory=True,
                                        header=0, chunksize=1000, na_values=['?', '', ' ']):
                processed_chunk = self._process_chunk(chunk, table, file)
                chunks.append(processed_chunk)
 
            df = pd.concat(chunks, ignore_index=True)
            df = df.dropna(how='all', axis=1)
            data_frames[table] = df

        return data_frames

    
    def __repr__(self):
        return 'RepairData()'
    

class FinancialDataBase:
    def __init__(self, data: dict):
        self.data = data
        self.engine = db.engines['statistics']
        self.upload_data()

    def upload_data(self) -> None:
        batch_size = 1000  # Adjust this value based on your memory constraints and performance needs
        with Session(self.engine) as session:
            try:
                for table, df in self.data.items():
                    for i in range(0, len(df), batch_size):
                        batch = df.iloc[i:i+batch_size]
                        session.bulk_insert_mappings(
                            table, 
                            batch.replace({np.nan: None}).to_dict(orient='records'))
                        session.commit() 
                        session.expire_all()  
                        
            except Exception as e:
                session.rollback()
                raise e


