import sqlalchemy, os
from dotenv import load_dotenv, set_key
from pathlib import Path

class Connection_to_db:
    def __init__(self):
        load_dotenv()
        p = Path('.env')
        if not p.exists():
            self.create_env_file(p)

        db_name = os.getenv('database_name')
        account_name = os.getenv('account_name')
        psw = os.getenv('password')

        url = f'postgresql+pg8000://{account_name}:{psw}@localhost/{db_name}'

        self._engine = sqlalchemy.create_engine(url)
        
    def create_env_file(self, p: Path) -> None:
        p.touch(mode=0o600, exist_ok=False)
        os.environ
        
        set_key(dotenv_path=p, key_to_set='database_name', value_to_set=input('database name: '))
        set_key(dotenv_path=p, key_to_set='account_name', value_to_set=input('account: '))
        set_key(dotenv_path=p, key_to_set='password', value_to_set=input('password: '))



    @property
    def engine(self):
        return self._engine

    def __repr__(self):
        return 'Connection_to_db()'