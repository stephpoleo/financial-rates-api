"""
Conexión a PostgreSQL con psycopg3.
"""

from contextlib import contextmanager
from typing import Generator

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from app.config import settings


# Pool de conexiones
pool: ConnectionPool | None = None


def init_pool() -> None:
    """Inicializa el pool de conexiones."""
    global pool
    if pool is None:
        pool = ConnectionPool(
            settings.DATABASE_URL,
            min_size=2,
            max_size=10,
            kwargs={"row_factory": dict_row}
        )


def close_pool() -> None:
    """Cierra el pool de conexiones."""
    global pool
    if pool is not None:
        pool.close()
        pool = None


@contextmanager
def get_connection() -> Generator[psycopg.Connection, None, None]:
    """
    Context manager para obtener una conexión del pool.

    Uso:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM cetes")
                rows = cur.fetchall()
    """
    if pool is None:
        init_pool()

    with pool.connection() as conn:
        yield conn


def get_db() -> Generator[psycopg.Connection, None, None]:
    """
    Dependency para FastAPI.

    Uso:
        @app.get("/endpoint")
        def endpoint(db: psycopg.Connection = Depends(get_db)):
            ...
    """
    if pool is None:
        init_pool()

    with pool.connection() as conn:
        yield conn
