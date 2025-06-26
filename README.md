# 🛠️ Odoo ETL & Analytics Pipeline

This project builds a complete data engineering pipeline using Odoo 15 as the data source. The pipeline extracts data via XML-RPC, transforms it using Python, loads it into PostgreSQL, and visualizes it through Apache Superset. All components are containerized using Docker and orchestrated via Apache Airflow.

---

## 📦 Features

- Odoo ERP (Sales, Inventory, Customers modules)
- XML-RPC data extraction
- Python ETL scripts
- PostgreSQL data warehouse
- Apache Airflow for orchestration
- Apache Superset dashboards
- Docker Compose deployment

---

## 🪰 Tech Stack

- Odoo 15 (Dockerized)
- Python 3
- PostgreSQL 13
- Apache Airflow 2.7
- Apache Superset 2.1
- Docker Compose

---

## 🚀 Quick Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/fatimahnaqib/odooops-insight.git
cd odooops-insight
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```env
ODOO_URL=http://localhost:8069
ODOO_DB=odooops_db
ODOO_USERNAME=odoo
ODOO_PASSWORD=odoo

PG_HOST=analytics-db
PG_PORT=5432
PG_DB=analytics
PG_USER=analyst
PG_PASSWORD=analyst
```

### 3. Build and Start the Containers

```bash
docker-compose up --build
```

This will:

- Start Odoo
- Initialize PostgreSQL databases
- Launch Airflow (scheduler + webserver)
- Launch Superset

### 4. Odoo Setup (Post-Docker Boot)

After running `docker-compose up --build`, follow these steps to initialize and populate Odoo with sample data:

## 🖥️ Open your browser and go to:
[http://localhost:8069](http://localhost:8069)

## 🧾 On the first load, you’ll see the Odoo database creation screen:

- **Database Name**: `odooops_db`
- **Email**: `odoo@example.com`
- **Password**: `odoo`
- **Confirm Password**: `odoo`
- **Language**: English
- **Country**: Your choice

**Uncheck** `"Load demonstration data"` if you're adding custom data.  
Click **Create database**.

---

## 🚪 Once logged in, install the required Odoo modules:

- **Sales**
- **Inventory**
- **Contacts**

Navigate to **Apps**, remove the “Apps” filter (if nothing shows up), then click **Install** on the modules listed.

---

## Create or import test data:

- Add a few **customers**
- Create a few **products**
- Make some **Sales Orders** using those products/customers

This manual setup populates the models used by the ETL pipeline:

- `res.partner`
- `product.product`
- `sale.order`
- `sale.order.line`

---

Once done, you're ready to trigger the ETL pipeline.


### 5. Set Up Airflow & Superset Automatically

Airflow admin credentials:

```pgsql
username: admin
password: admin
```

Superset admin credentials:

```pgsql
username: admin
password: admin
```

### 6. Trigger the ETL Pipeline (Optional)

If you're not using Airflow UI yet, run:

```bash
docker exec -it <airflow-webserver-container-name> bash
python3 -m etl.run_extracts
python3 -m etl.load_to_postgres
```

Otherwise, trigger it via the Airflow web UI: [http://localhost:8080](http://localhost:8080)

---

## 🥪 Directory Structure

```bash
odooops-insight/
├── airflow_dags/           # DAGs for Airflow
│   └── odoo_etl_dags.py    # Main ETL DAG
├── config/                 # Configuration settings
│   ├── __init__.py
│   └── config.py           # Environment variable loader
├── etl/                    # ETL scripts
│   ├── __init__.py
│   ├── connector.py        # Odoo XML-RPC connector
│   ├── extractor.py        # Data extractor logic
│   ├── transform.py        # Data transformations
│   ├── load_to_postgres.py # Load to PostgreSQL
│   └── run_extracts.py     # ETL runner script
├── logs/                   # Airflow logs
├── odoo/                   # Odoo addons (optional)
├── outputs/                # CSV outputs from ETL
├── tests/                  # Tests ETL
├── .env                    # Environment variables (not committed)
├── docker-compose.yml      # Docker Compose config
├── README.md               # This file
└── requirements.txt        # Python dependencies
```
---

## 📊 Superset Setup Notes

After Superset starts, go to [http://localhost:8088](http://localhost:8088) and log in,then:

1. Go to Settings > Database Connections
2. Click + Database
3. Use these credentials:

```yaml
Host: analytics-db
Port: 5432
Database: analytics
Username: analyst
Password: analyst
```
4. Click Connect
5. Import tables and create charts/dashboards

---

## 👩‍💻 Author

**Fatimah Naqib** – Backend Engineer | Data Engineer

---
