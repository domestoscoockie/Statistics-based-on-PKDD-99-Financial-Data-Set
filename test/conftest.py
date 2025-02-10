import pytest
from unittest.mock import patch, Mock
from connection import Connection_to_db


@pytest.fixture(scope='session',autouse=True)
def connection_obj():
    con = Connection_to_db()
    return con