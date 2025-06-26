# config/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Odoo connection
ODOO_URL = os.getenv("ODOO_URL", "http://localhost:8069")
ODOO_DB = os.getenv("ODOO_DB", "odooops_db")
ODOO_USERNAME = os.getenv("ODOO_USERNAME", "odoo")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", "odoo")

# PostgreSQL connection for analytics
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "analytics")
PG_USER = os.getenv("PG_USER", "analyst")
PG_PASSWORD = os.getenv("PG_PASSWORD", "analyst")
