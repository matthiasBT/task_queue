from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

DB_HOST = '127.0.0.1'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'  # for test purposes only
DB_DATABASE_NAME = 'postgres'

DB_MAX_CONN = 2
DB_MIN_CONN = 1

CONN_POOL = ThreadedConnectionPool(
    DB_MIN_CONN, DB_MAX_CONN,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_DATABASE_NAME
)


@contextmanager
def get_conn():
    connection = CONN_POOL.getconn()
    yield connection
    CONN_POOL.putconn(connection)


@contextmanager
def get_db_cursor():
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        yield cursor
        conn.commit()
        cursor.close()


def execute(query):
    with get_db_cursor() as cursor:
        cursor.execute(query)
        # in this app all queries operate on single rows
        return cursor.fetchone()
