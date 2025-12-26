# Google Shop End-to-End Analytics Pipeline

A full-cycle data engineering project implementing an automated ELT pipeline: from raw data extraction (BigQuery) to final business intelligence dashboards (Apache Superset).

## 1. Project Overview
This project demonstrates the orchestration of a modern data stack. It extracts raw e-commerce data, loads it into a containerized PostgreSQL warehouse, transforms it using dbt best practices, and visualizes key business metrics like Revenue and Average Order Value (AOV).

## 2. Tech Stack
* **Python (Pandas)** – Custom extraction logic from Google BigQuery API.
* **PostgreSQL (Docker)** – Primary Data Warehouse (DWH) for storing raw and transformed data.
* **dbt (Data Build Tool)** – Transformation layer implementing modular SQL, staging/marts architecture, and data quality tests.
* **Apache Superset** – Modern BI tool for creating interactive dashboards.
* **Docker & Docker Compose** – Infrastructure orchestration and environment isolation.

## 3. Project Architecture
The pipeline follows the **ELT (Extract, Load, Transform)** pattern:

1.  **Extract & Load:** A Python-based ingestion script fetches raw e-commerce data from BigQuery and loads it into the `public` schema of the PostgreSQL warehouse.
2.  **Transform:** `dbt` processes the raw data through two main layers:
    * **Staging**: Data cleaning and type casting.
    * **Marts**: Building business-ready entities (e.g., `fct_country_performance`) in the `analytics` schema.
3.  **Visualize:** Superset connects to the `analytics` schema to serve business-critical metrics.



## 4. Key Metrics & Insights
* **Total Revenue:** Gross sales tracking across various timeframes and regions.
* **Average Order Value (AOV):** Implemented as a dynamic semantic metric: 
  $$AOV = \frac{\sum \text{Total Revenue}}{\sum \text{Total Orders}}$$
* **Geospatial Performance:** Identification of high-performing markets via country-level aggregation.

## 5. Getting Started

### Prerequisites
* Docker & Docker Compose installed.
* Python 3.9+ environment.
* BigQuery Service Account credentials (JSON).

### Step-by-Step Installation
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/your-username/google-shop-pipeline.git](https://github.com/your-username/google-shop-pipeline.git)
    cd google-shop-pipeline
    ```

2.  **Configure Environment Variables:**
    Create a `.env` file from the example:
    ```bash
    cp env.example .env
    # Edit .env with your PostgreSQL credentials
    ```

3.  **Spin Up Infrastructure:**
    ```bash
    docker-compose up -d
    ```

4.  **Execute Data Transformations:**
    Navigate to the dbt directory and run:
    ```bash
    dbt deps
    dbt build
    ```

5.  **Access Dashboards:**
    Open [http://localhost:8088](http://localhost:8088) in your browser.

## 6. Project Structure
```text
├── extract_load/        # Python ingestion scripts
├── dbt_project/         # dbt models, seeds, and snapshots
│   ├── models/
│   │   ├── staging/     # Raw data cleaning
│   │   └── marts/       # Business intelligence tables
├── superset/            # Dashboard exports and Superset configs
├── docker-compose.yml   # Infrastructure definition
└── README.md            # Project documentation