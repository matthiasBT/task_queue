from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from psycopg2 import OperationalError
from contextlib import contextmanager
from time import sleep

DB_HOST = 'postgres'
DB_PORT = 5432
DB_USER = 'postgres'
DB_PASSWORD = 'mysecretpassword'  # for test purposes only
DB_DATABASE_NAME = 'postgres'

DB_MAX_CONN = 2
DB_MIN_CONN = 1


def get_pool():
    """ Initialize connection pool

    It may take some time for the database to start up, so it's necessary
    to retry the request until it succeeds.
    """
    attempts = 0
    while True:
        try:
            pool = ThreadedConnectionPool(
                DB_MIN_CONN, DB_MAX_CONN,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
                database=DB_DATABASE_NAME
            )
            return pool
        except OperationalError:
            sleep(2 ** attempts)  # exponential backoff
            attempts += 1


CONN_POOL = get_pool()


@contextmanager
def get_conn():
    connection = CONN_POOL.getconn()
    yield connection
    connection.commit()
    CONN_POOL.putconn(connection)


@contextmanager
def get_db_cursor():
    with get_conn() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        yield cursor
        cursor.close()


def execute(query, args=None, logger=None):
    """ Execute a query and return the result """
    with get_db_cursor() as cursor:
        if args:
            cursor.execute(query, args)
        else:
            cursor.execute(query)
        if logger:
            logger.info(cursor.query.decode())
        # in this app all queries operate on single rows
        return cursor.fetchone()
