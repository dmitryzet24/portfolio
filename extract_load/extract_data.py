import os
import pandas as pd
from google.cloud import bigquery
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Environmental variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google_creds.json"

def extract_and_load():
    client = bigquery.Client()

    query="""
    SELECT
        visitId,
        visitStartTime,
        date,
        device.browser as browser,
        device.deviceCategory as device_type,
        geoNetwork.country as country,
        totals.pageviews as pageviews,
        totals.transactions as transactions,
        totals.transactionRevenue / 1000000 as revenue_usd
        FROM
            `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
        WHERE
            totals.transactions IS NOT NULL
        LIMIT 1000;
    """
    print("Connecting to BigQuery...")
    try:
        df = client.query(query).to_dataframe()
        print(f"Got lines: {len(df)}")
    except Exception as e:
        print(f"BigQuery Error: {e}")
        return

    #Postgres connection port:5433
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")

    #SQLAlchemy engine
    engine = create_engine(f"postgresql://{user}:{password}@localhost:5433/{db}")
    print("Loading data to Postgres (RAW data layer)...")
    try:
        df.to_sql("raw_google_transactions", engine, if_exists="replace", index=False)
        print("Data successfully loaded to table 'raw_google_transactions'")
    except Exception as e:
        print("Error loading data to Postgres: {e} ")

if __name__ ==  "__main__":
    extract_and_load()