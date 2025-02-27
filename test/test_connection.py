import pytest
from pathlib import Path
from unittest.mock import patch, Mock
from trash.connection import Connection_to_db
import tempfile

class TestConnection:


    @patch('pathlib.Path.exists', return_value=True)
    def test_file_exists(self, mock_exist: Mock):
        with tempfile.NamedTemporaryFile(suffix='.env',delete=False) as temp:
            temp_path = Path(temp.name)
            with patch('connection.Path', return_value=temp_path):
                con = Connection_to_db()
                mock_exist.assert_called_once()
        temp_path.unlink()    


    @patch('pathlib.Path.exists', return_value=False)
    def test_file_not_exists(self, mock_exist: Mock):
        with tempfile.NamedTemporaryFile(suffix='.env',delete=False) as temp:
            temp_path = Path(temp.name)
            with patch('connection.Path', return_value=temp_path):
                with pytest.raises(FileExistsError):
                    con = Connection_to_db()
        temp_path.unlink()    


    @patch('pathlib.Path.exists', return_value=False)
    @patch('pathlib.Path.touch')
    @patch('builtins.input', side_effect=['test_db', 'test_user', 'test_password'])
    def test_env_creation(self, mock_input: Mock, mock_touch: Mock, mock_exists: Mock):
        with tempfile.NamedTemporaryFile(suffix='.env',delete=False) as temp:
            temp_path = Path(temp.name)
            with patch('connection.Path', return_value=temp_path): 
                con = Connection_to_db()
                
                #dot.env uses Path.touch to rewrite .env file so every time its called in the bottom of this Path.touch is called
                #thats why we have to check if its called 4 times
                assert mock_touch.call_count == 4 

        temp_path.unlink()


    @patch('pathlib.Path.exists', return_value=True)
    @patch('dotenv.load_dotenv', return_value=True)
    def test_is_env_file(self, mock_load_dotenv: Mock, mock_exist: Mock):
        conn = Connection_to_db()
        mock_exist.assert_called_once()
        assert mock_load_dotenv.return_value == True


    @patch('pathlib.Path.exists', return_value = True)
    @patch('dotenv.set_key')
    @patch('os.getenv', side_effect=['test_db', 'test_user', 'test_password'])
    @patch('sqlalchemy.create_engine')
    def test_crete_engine(self,mock_create_eng: Mock, mock_input: Mock, mock_set_key: Mock, mock_exists: Mock):
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_path = Path(temp.name)
            temp.close()
            with patch('connection.Path', return_value=temp_path): 
                con = Connection_to_db()

                mock_create_eng.assert_called_once_with('postgresql+pg8000://test_user:test_password@localhost/test_db')
                