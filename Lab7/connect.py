import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
    )
        return conn
    except psycopg2.OperationalError as e:
        print(f"[ERROR] Could not connect to the database: {e}")
        raise
def get_cursor(conn):
    """Return a cursor from the given connection."""
    return conn.cursor()
 