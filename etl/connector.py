# etl/connector.py
import xmlrpc.client
import logging
from typing import List, Optional, Any, Dict

logger = logging.getLogger(__name__)

class OdooConnector:
    """Handles authentication and queries to Odoo via XML-RPC"""

    def __init__(self, url: str, db: str, username: str, password: str) -> None:
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid: Optional[int] = None

        self.common = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/common")
        self.models = xmlrpc.client.ServerProxy(f"{self.url}/xmlrpc/2/object")
        self.authenticate()

    def authenticate(self) -> None:
        try:
            self.uid = self.common.authenticate(self.db, self.username, self.password, {})
            if not self.uid:
                raise ConnectionError("Authentication failed. Check credentials.")
            logger.info(f"Authenticated to Odoo with uid: {self.uid}")
        except Exception as e:
            logger.error(f"Failed to authenticate to Odoo: {e}")
            raise

    def fetch_all_records(
        self,
        model: str,
        fields: Optional[List[str]] = None,
        domain: Optional[List[Any]] = None,
        batch_size: int = 1000,
        additional_filter: Optional[List[Any]] = None
    ) -> List[Any]:
        """
        Fetch all records for a model in batches with optional incremental filter.

        Params:
        - model: Odoo model name
        - fields: list of fields to fetch
        - domain: base domain filters (list)
        - batch_size: batch size per request
        - additional_filter: extra domain filters (e.g. date filters for incremental load)

        Returns:
        - list of all matching records
        """
        domain = domain or []
        if additional_filter:
            domain = domain + additional_filter

        fields = fields or []

        all_records = []
        offset = 0
        while True:
            try:
                batch = self.models.execute_kw(
                    self.db,
                    self.uid,
                    self.password,
                    model,
                    "search_read",
                    [domain],
                    {"fields": fields, "limit": batch_size, "offset": offset}
                )
            except Exception as e:
                logger.error(f"Error fetching batch from model '{model}': {e}")
                raise

            if not batch:
                break

            all_records.extend(batch)
            offset += batch_size
            logger.info(f"Fetched batch of {len(batch)} from '{model}', offset {offset}")

        logger.info(f"Total records fetched from '{model}': {len(all_records)}")
        return all_records
