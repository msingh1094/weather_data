import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Construct the database connection string from environment variables
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def create_tables():
    """Creates the weather_data and yearly_weather_stats tables."""
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Create weather_data table
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            station_id TEXT NOT NULL,
            date DATE NOT NULL,
            max_temp REAL,
            min_temp REAL,
            precipitation REAL
        );
    """)

    # Create yearly_weather_stats table
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS yearly_weather_stats (
            station_id VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            avg_max_temp FLOAT,
            avg_min_temp FLOAT,
            total_precipitation FLOAT,
            PRIMARY KEY (station_id, year)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()
