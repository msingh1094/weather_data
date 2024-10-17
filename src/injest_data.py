import os
from datetime import datetime
import pandas as pd
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

load_dotenv()

# Database connection details from environment variables
DATABASE_URL = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def get_db_connection():
    """Establishes a connection to the PostgreSQL database."""
    conn = psycopg2.connect(**DATABASE_URL)
    return conn

def ingest_weather_data(conn, data_dir):
    """Ingests weather data from text files into the PostgreSQL database."""
    start_time = datetime.now()
    total_records_ingested = 0

    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            df = pd.read_csv(os.path.join(data_dir, filename), sep='\t', header=None,
                             names=['date', 'max_temp', 'min_temp', 'precipitation'])
            df['station_id'] = filename[:-4]
            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
            df = df.replace(-9999, None)
            df[['max_temp', 'min_temp', 'precipitation']] = df[['max_temp', 'min_temp', 'precipitation']] / 10
            
            # Prepare data for bulk insert
            data = list(df.itertuples(index=False, name=None))
            
            try:
                with conn.cursor() as cur:
                    # Bulk insert using psycopg2.extras.execute_values for performance
                    insert_query = """
                        INSERT INTO weather_data (date, max_temp, min_temp, precipitation, station_id)
                        VALUES %s
                    """
                    extras.execute_values(cur, insert_query, data)
                    conn.commit()
                    total_records_ingested += len(df)
            except Exception as e:
                conn.rollback()
                print(f"Error inserting data from file {filename}: {e}")

    end_time = datetime.now()
    print(f"Data ingestion complete. Time taken: {end_time - start_time}. Records ingested: {total_records_ingested}")

if __name__ == '__main__':
    with get_db_connection() as conn:
        ingest_weather_data(conn, 'data/wx_data')  # Adjust data directory path if needed
        

