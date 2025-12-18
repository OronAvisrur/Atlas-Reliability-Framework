import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

from backend.core.config import settings


def get_connection():
    return psycopg2.connect(settings.database_url)


@contextmanager
def get_db():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)