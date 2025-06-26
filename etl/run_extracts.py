from typing import NoReturn
import os
import pandas as pd
import logging
from datetime import datetime

from .extractor import OdooDataExtractor
from .transform import (
    transform_sales_orders,
    transform_products,
    transform_customers,
    transform_order_lines
)

logger = logging.getLogger(__name__)

LAST_EXTRACT_FILE = "outputs/last_extract_timestamp.txt"

def read_last_extract_timestamp() -> str:
    """Read last extraction timestamp from a file, or return a default old timestamp"""
    if os.path.exists(LAST_EXTRACT_FILE):
        with open(LAST_EXTRACT_FILE, "r") as f:
            ts = f.read().strip()
            logger.info(f"Last extract timestamp read: {ts}")
            return ts
    else:
        # default far past timestamp to extract all on first run
        default_ts = "1970-01-01 00:00:00"
        logger.info(f"No last extract timestamp found, using default {default_ts}")
        return default_ts

def write_last_extract_timestamp(ts: str) -> None:
    """Write the latest extraction timestamp to a file"""
    with open(LAST_EXTRACT_FILE, "w") as f:
        f.write(ts)
    logger.info(f"Updated last extract timestamp to: {ts}")

def main() -> NoReturn:
    extractor = OdooDataExtractor()
    os.makedirs("outputs", exist_ok=True)

    last_extract_ts = read_last_extract_timestamp()

    # --- Sales Orders ---
    # Incremental filter: fetch records updated since last extract
    sales_domain = []
    sales_incremental_filter = [('write_date', '>=', last_extract_ts)]
    df_sales = pd.DataFrame(extractor.connector.fetch_all_records(
        model="sale.order",
        fields=["id", "name", "partner_id", "amount_total", "state", "date_order", "write_date"],
        domain=sales_domain,
        additional_filter=sales_incremental_filter,
        batch_size=1000
    ))
    if not df_sales.empty:
        df_sales = transform_sales_orders(df_sales)
        df_sales.to_csv("outputs/sales_orders.csv", index=False)
        logger.info("Transformed & saved sales_orders.csv")
    else:
        logger.info("No new sales orders to extract.")

    # --- Products ---
    # For products, you can also apply incremental filter on 'write_date' if desired
    products_incremental_filter = [('write_date', '>=', last_extract_ts)]
    df_products = pd.DataFrame(extractor.connector.fetch_all_records(
        model="product.product",
        fields=["id", "name", "default_code", "list_price", "write_date"],
        additional_filter=products_incremental_filter,
        batch_size=1000
    ))
    if not df_products.empty:
        df_products = transform_products(df_products)
        df_products.to_csv("outputs/products.csv", index=False)
        logger.info("Transformed & saved products.csv")
    else:
        logger.info("No new products to extract.")

    # --- Customers ---
    customers_domain = [("customer_rank", ">", 0)]
    customers_incremental_filter = [('write_date', '>=', last_extract_ts)]
    df_customers = pd.DataFrame(extractor.connector.fetch_all_records(
        model="res.partner",
        domain=customers_domain,
        fields=["id", "name", "email", "phone", "city", "country_id", "write_date"],
        additional_filter=customers_incremental_filter,
        batch_size=1000
    ))
    if not df_customers.empty:
        df_customers = transform_customers(df_customers)
        df_customers.to_csv("outputs/customers.csv", index=False)
        logger.info("Transformed & saved customers.csv")
    else:
        logger.info("No new customers to extract.")

    # --- Order Lines ---
    order_lines_incremental_filter = [('write_date', '>=', last_extract_ts)]
    df_lines = pd.DataFrame(extractor.connector.fetch_all_records(
        model="sale.order.line",
        fields=["order_id", "product_id", "product_uom_qty", "price_unit", "price_subtotal", "write_date"],
        additional_filter=order_lines_incremental_filter,
        batch_size=1000
    ))
    if not df_lines.empty:
        df_lines = transform_order_lines(df_lines)
        df_lines.to_csv("outputs/order_lines.csv", index=False)
        logger.info("Transformed & saved order_lines.csv")
    else:
        logger.info("No new order lines to extract.")

    # Update last extract timestamp to current UTC time (ISO format)
    new_extract_ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    write_last_extract_timestamp(new_extract_ts)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
