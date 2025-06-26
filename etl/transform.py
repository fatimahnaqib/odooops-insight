import pandas as pd
import ast
from typing import Optional

def extract_id(val: Optional[str]) -> Optional[int]:
    try:
        return ast.literal_eval(str(val))[0]
    except Exception:
        return None

def extract_name(val: Optional[str]) -> Optional[str]:
    try:
        return ast.literal_eval(str(val))[1]
    except Exception:
        return None

def transform_sales_orders(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["customer_id"] = df["partner_id"].apply(extract_id)
    df["customer_name"] = df["partner_id"].apply(extract_name)
    df = df.drop(columns=["partner_id"])

    df["date_order"] = pd.to_datetime(df["date_order"])
    df["order_month"] = df["date_order"].dt.to_period("M").astype(str)

    def bucket(amount: float) -> str:
        if amount < 500:
            return "low"
        elif amount < 1500:
            return "medium"
        else:
            return "high"

    df["revenue_bucket"] = df["amount_total"].apply(bucket)
    return df

def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    return df.copy()

def transform_customers(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["country_name"] = df["country_id"].apply(extract_name)
    df = df.drop(columns=["country_id"])
    return df

def transform_order_lines(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["order_id"] = df["order_id"].apply(extract_id)
    df["product_id"] = df["product_id"].apply(extract_id)
    return df
