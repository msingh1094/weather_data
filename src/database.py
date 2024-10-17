import psycopg2

DATABASE_URL = 'postgresql://weather_user:root@localhost:5432/weather_data' 

def get_db_connection():
    """Returns a new database connection."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn