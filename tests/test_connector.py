# tests/test_connector.py
import pytest
from unittest.mock import MagicMock, patch
from etl.connector import OdooConnector

@patch("etl.connector.xmlrpc.client.ServerProxy")
def test_authenticate_success(mock_server_proxy):
    mock_common = MagicMock()
    mock_common.authenticate.return_value = 123
    mock_server_proxy.return_value = mock_common

    conn = OdooConnector("http://localhost:8069", "test_db", "user", "pass")
    assert conn.uid == 123
    