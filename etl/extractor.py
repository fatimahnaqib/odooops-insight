# etl/extractor.py
from typing import List, Optional
import os
import pandas as pd
import logging

from .connector import OdooConnector
from config import config

logger = logging.getLogger(__name__)

class OdooDataExtractor:
    def __init__(self) -> None:
        self.connector = OdooConnector(
            url=config.ODOO_URL,
            db=config.ODOO_DB,
            username=config.ODOO_USERNAME,
            password=config.ODOO_PASSWORD
        )

    def extract(self, model: str, fields: List[str], domain: Optional[List] = None, limit: int = 100) -> pd.DataFrame:
        records = self.connector.fetch_records(model=model, domain=domain, fields=fields, limit=limit)
        if not records:
            logger.warning(f"No records found for model '{model}'.")
        df = pd.DataFrame(records)
        return df

    def extract_and_save(self, model: str, fields: List[str], filename: str, domain: Optional[List] = None, limit: int = 100) -> None:
        df = self.extract(model, fields, domain, limit)
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", filename)
        df.to_csv(path, index=False)
        logger.info(f"Extracted '{model}' and saved to '{path}'.")
