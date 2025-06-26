import pandas as pd
from etl.load_to_postgres import PostgresLoader
from unittest.mock import MagicMock, patch

@patch("etl.load_to_postgres.psycopg2.connect")
def test_create_tables_called(mock_connect):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    loader = PostgresLoader()
    mock_cursor.execute.assert_called()  # At least called once
