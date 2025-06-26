import pandas as pd
from etl.transform import transform_sales_orders, extract_id, extract_name

def test_extract_id_and_name():
    val = str([5, "Alice"])
    assert extract_id(val) == 5
    assert extract_name(val) == "Alice"

def test_transform_sales_orders():
    data = {
        "id": [1],
        "name": ["SO001"],
        "partner_id": [str([10, "John Doe"])],
        "amount_total": [1600],
        "state": ["sale"],
        "date_order": ["2024-05-01 10:00:00"]
    }
    df = pd.DataFrame(data)
    df_transformed = transform_sales_orders(df)
    assert "customer_id" in df_transformed
    assert df_transformed["revenue_bucket"].iloc[0] == "high"
