import pandas as pd
from unittest.mock import patch, MagicMock
from etl.load_to_postgres import PostgresLoader


@patch("etl.load_to_postgres.psycopg2.connect")
@patch("etl.load_to_postgres.pd.read_csv")
@patch("etl.load_to_postgres.execute_batch")
def test_insert_customers_success(mock_execute_batch, mock_read_csv, mock_connect):
    sample_data = pd.DataFrame([{
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
        "phone": "123456",
        "city": "New York",
        "country_name": "USA"
    }])
    mock_read_csv.return_value = sample_data

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    loader = PostgresLoader()
    loader.insert_customers("fake_path.csv")

    expected_sql = """
        INSERT INTO customers (id, name, email, phone, city, country_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
    expected_records = [(1, "Alice", "alice@example.com", "123456", "New York", "USA")]

    mock_execute_batch.assert_called_once_with(mock_cursor, expected_sql, expected_records)
    assert mock_conn.commit.call_count >= 1

@patch("etl.load_to_postgres.psycopg2.connect")
@patch("etl.load_to_postgres.pd.read_csv")
@patch("etl.load_to_postgres.execute_batch")
def test_insert_products_success(mock_execute_batch, mock_read_csv, mock_connect):
    sample_data = pd.DataFrame([{
        "id": 201,
        "name": "Notebook",
        "default_code": "NB123",
        "list_price": 9.99
    }])
    mock_read_csv.return_value = sample_data

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    loader = PostgresLoader()
    loader.insert_products("fake_path.csv")

    expected_sql = """
        INSERT INTO products (id, name, default_code, list_price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
    expected_records = [(201, "Notebook", "NB123", 9.99)]

    mock_execute_batch.assert_called_once_with(mock_cursor, expected_sql, expected_records)
    assert mock_conn.commit.call_count >= 1


@patch("etl.load_to_postgres.psycopg2.connect")
@patch("etl.load_to_postgres.pd.read_csv")
@patch("etl.load_to_postgres.execute_batch")
def test_insert_sales_orders_success(mock_execute_batch, mock_read_csv, mock_connect):
    sample_data = pd.DataFrame([{
        "id": 301,
        "name": "SO123",
        "customer_id": 10,
        "customer_name": "Alice",
        "amount_total": 1234.56,
        "state": "sale",
        "date_order": "2024-06-01 12:00:00",
        "order_month": "2024-06",
        "revenue_bucket": "medium"
    }])
    mock_read_csv.return_value = sample_data

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    loader = PostgresLoader()
    loader.insert_sales_orders("fake_path.csv")

    expected_sql = """
        INSERT INTO sales_orders (
            id, name, customer_id, customer_name, amount_total,
            state, date_order, order_month, revenue_bucket
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
    expected_records = [(301, "SO123", 10, "Alice", 1234.56, "sale", "2024-06-01 12:00:00", "2024-06", "medium")]

    mock_execute_batch.assert_called_once_with(mock_cursor, expected_sql, expected_records)
    assert mock_conn.commit.call_count >= 1

@patch("etl.load_to_postgres.psycopg2.connect")
@patch("etl.load_to_postgres.pd.read_csv")
@patch("etl.load_to_postgres.execute_batch")
def test_insert_order_lines_success(mock_execute_batch, mock_read_csv, mock_connect):
    sample_data = pd.DataFrame([{
        "order_id": 301,
        "product_id": 201,
        "product_uom_qty": 2,
        "price_unit": 5.00,
        "price_subtotal": 10.00
    }])
    mock_read_csv.return_value = sample_data

    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    loader = PostgresLoader()
    loader.insert_order_lines("fake_path.csv")

    expected_sql = """
        INSERT INTO order_lines (
            order_id, product_id, product_uom_qty, price_unit, price_subtotal
        )
        VALUES (%s, %s, %s, %s, %s);
        """
    expected_records = [(301, 201, 2, 5.00, 10.00)]

    mock_execute_batch.assert_called_once_with(mock_cursor, expected_sql, expected_records)
    assert mock_conn.commit.call_count >= 1  
       