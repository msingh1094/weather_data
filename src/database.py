import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Construct the database connection string from environment variables
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def get_db_connection():
    """Returns a new database connection."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn