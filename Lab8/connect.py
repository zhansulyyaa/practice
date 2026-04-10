import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

def connect():
    """Connect to the PostgreSQL database server."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(f"Connection error: {error}")
        return None
