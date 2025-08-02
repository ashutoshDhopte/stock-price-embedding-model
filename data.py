import psycopg2
import numpy as np
import os
from dotenv import load_dotenv

def connect_to_postgres():
    """Connects to the PostgreSQL database using environment variables."""
    load_dotenv() # Load variables from .env file
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        print("✅ Successfully connected to PostgreSQL.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ Could not connect to PostgreSQL: {e}")
        return None

def fetch_ohlcv_data(conn, ticker):
    """Fetches the latest OHLCV data for a given ticker."""
    cursor = None
    try:
        cursor = conn.cursor()
        query = """
            SELECT timestamp, open, high, low, close, volume
            FROM stock_ohlcv
            WHERE stock_name = %s
            ORDER BY timestamp DESC;
        """
        cursor.execute(query, (ticker,))
        data = cursor.fetchall()
        print(f"✅ Fetched {len(data)} records for ticker '{ticker}'.")
        return data
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return []
    finally:
        if cursor:
            cursor.close()


