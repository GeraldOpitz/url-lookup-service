import os
import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres"),
        dbname=os.getenv("POSTGRES_DB", "url_lookup"),
    )


def get_malicious_urls_from_db() -> set[str]:
    """
    Returns the set of malicious URLs stored in the database.
    Raises an exception if the database is unavailable.
    """
    conn = get_db_connection()

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT url FROM malicious_urls")
            rows = cursor.fetchall()
            return {row[0] for row in rows}
    finally:
        conn.close()
