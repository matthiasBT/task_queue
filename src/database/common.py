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


def get_cursor(connection):
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    yield cursor
    cursor.close()


@contextmanager
def get_db_cursor(connection):
    if connection is not None:
        yield from get_cursor(connection)
    else:
        with get_conn() as conn:
            yield from get_cursor(conn)


def execute(query, params=None, connection=None, logger=None, fetch=True):
    """ Execute a query and return the result """
    with get_db_cursor(connection) as cursor:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if logger:
            logger.info(cursor.query.decode())
        # in this app all queries operate on single rows
        if fetch:
            return cursor.fetchone()
