# etl/load_to_postgres.py
from typing import Optional
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from config import config
import logging
import numpy as np
from typing import List, Tuple


logger = logging.getLogger(__name__)

class PostgresLoader:
    def __init__(self) -> None:
        self.conn: Optional[psycopg2.extensions.connection] = None
        self.cur: Optional[psycopg2.extensions.cursor] = None
        self.connect()
        self.create_tables()

    def connect(self) -> None:
        try:
            self.conn = psycopg2.connect(
                host=config.PG_HOST,
                dbname=config.PG_DB,
                port=config.PG_PORT,
                user=config.PG_USER,
                password=config.PG_PASSWORD
            )
            self.cur = self.conn.cursor()
            logger.info("Connected to PostgreSQL database.")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {e}")
            raise

    def create_tables(self) -> None:
        create_customers = """
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            city TEXT,
            country_name TEXT
        );"""
        create_products = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            default_code TEXT,
            list_price NUMERIC(10, 2)
        );"""
        create_sales_orders = """
        CREATE TABLE IF NOT EXISTS sales_orders (
            id INTEGER PRIMARY KEY,
            name TEXT,
            customer_id INTEGER,
            customer_name TEXT,
            amount_total NUMERIC(10, 2),
            state TEXT,
            date_order TIMESTAMP,
            order_month TEXT,
            revenue_bucket TEXT
        );"""
        create_order_lines = """
        CREATE TABLE IF NOT EXISTS order_lines (
            order_id INTEGER,
            product_id INTEGER,
            product_uom_qty NUMERIC,
            price_unit NUMERIC(10, 2),
            price_subtotal NUMERIC(10, 2)
        );"""
        try:
            self.cur.execute(create_customers)
            self.cur.execute(create_products)
            self.cur.execute(create_sales_orders)
            self.cur.execute(create_order_lines)
            self.conn.commit()
            logger.info("Tables created/verified successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            self.conn.rollback()
            raise

    def _prepare_records(self, df: pd.DataFrame) -> List[Tuple]:
        """
        Convert dataframe rows to list of tuples with native Python types.
        Handles numpy types and missing values.
        """
        return [
            tuple(
                None if pd.isna(x) else x.item() if isinstance(x, (np.integer, np.floating)) else x
                for x in row
            )
            for row in df.itertuples(index=False, name=None)
        ]
    
    def insert_customers(self, filepath: str) -> None:
        df = pd.read_csv(filepath)
        df = df[["id", "name", "email", "phone", "city", "country_name"]]
        records = self._prepare_records(df)
        sql = """
        INSERT INTO customers (id, name, email, phone, city, country_name)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        try:
            execute_batch(self.cur, sql, records)
            self.conn.commit()
            logger.info(f"Inserted {len(records)} customers.")
        except Exception as e:
            logger.error(f"Failed to insert customers: {e}")
            self.conn.rollback()
            raise

    def insert_products(self, filepath: str) -> None:
        df = pd.read_csv(filepath)
        df = df[["id", "name", "default_code", "list_price"]]
        records = self._prepare_records(df)
        sql = """
        INSERT INTO products (id, name, default_code, list_price)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        try:
            execute_batch(self.cur, sql, records)
            self.conn.commit()
            logger.info(f"Inserted {len(records)} products.")
        except Exception as e:
            logger.error(f"Failed to insert products: {e}")
            self.conn.rollback()
            raise

    def insert_sales_orders(self, filepath: str) -> None:
        df = pd.read_csv(filepath)
        df = df[[
            "id", "name", "customer_id", "customer_name", "amount_total",
            "state", "date_order", "order_month", "revenue_bucket"
        ]]
        records = self._prepare_records(df)

        sql = """
        INSERT INTO sales_orders (
            id, name, customer_id, customer_name, amount_total,
            state, date_order, order_month, revenue_bucket
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        try:
            execute_batch(self.cur, sql, records)
            self.conn.commit()
            logger.info(f"Inserted {len(records)} sales orders.")
        except Exception as e:
            logger.error(f"Failed to insert sales orders: {e}")
            self.conn.rollback()
            raise

    def insert_order_lines(self, filepath: str) -> None:
        df = pd.read_csv(filepath)
        df = df[["order_id", "product_id", "product_uom_qty", "price_unit", "price_subtotal"]]
        records = self._prepare_records(df)
        sql = """
        INSERT INTO order_lines (
            order_id, product_id, product_uom_qty, price_unit, price_subtotal
        )
        VALUES (%s, %s, %s, %s, %s);
        """
        try:
            execute_batch(self.cur, sql, records)
            self.conn.commit()
            logger.info(f"Inserted {len(records)} order lines.")
        except Exception as e:
            logger.error(f"Failed to insert order lines: {e}")
            self.conn.rollback()
            raise

    def close(self) -> None:
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("PostgreSQL connection closed.")

def run_load_to_postgres():
    try:
        loader = PostgresLoader()
        loader.insert_customers("outputs/customers.csv")
        loader.insert_products("outputs/products.csv")
        loader.insert_sales_orders("outputs/sales_orders.csv")
        loader.insert_order_lines("outputs/order_lines.csv")
    finally:
        loader.close()
        print("✅ Data loaded into PostgreSQL (analytics) successfully.")

# Allow CLI execution
if __name__ == "__main__":
    run_load_to_postgres()
