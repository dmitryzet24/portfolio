import os
import pandas as pd
from sqlalchemy import create_engine, text
from google.cloud import bigquery
from dotenv import load_dotenv

# Environmental variables
load_dotenv()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/extract_load/google_creds.json"

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
            `bigquery-public-data.google_analytics_sample.ga_sessions_*`
        WHERE
            _TABLE_SUFFIX BETWEEN '20160801' AND '20180830'
            AND totals.transactions IS NOT NULL
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
    engine = create_engine(f"postgresql://{user}:{password}@db:5432/{db}")
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            print("Truncating data...")
            conn.execute(text("TRUNCATE TABLE raw_google_transactions"))
            trans.commit()
        except:
            trans.rollback()
            raise

    print("Loading data to Postgres (RAW data layer)...")
    try:
        df.to_sql("raw_google_transactions", engine, if_exists="append", index=False)
        print("Data successfully loaded to table 'raw_google_transactions'")
    except Exception as e:
        print(f"Error loading data to Postgres: {e} ")

if __name__ ==  "__main__":
    extract_and_load()