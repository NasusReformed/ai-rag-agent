from typing import Any, Optional, Sequence

from pgvector.psycopg import register_vector
from psycopg_pool import ConnectionPool
from psycopg.rows import dict_row
from psycopg.types.json import Json


_pool: Optional[ConnectionPool] = None


def init_pool(dsn: str) -> None:
    global _pool
    if _pool is not None:
        return
    _pool = ConnectionPool(conninfo=dsn, min_size=1, max_size=5)
    with _pool.connection() as conn:
        register_vector(conn)


def close_pool() -> None:
    global _pool
    if _pool is not None:
        _pool.close()
        _pool = None


def _get_pool() -> ConnectionPool:
    if _pool is None:
        raise RuntimeError("DB pool not initialized")
    return _pool


def db_execute(query: str, params: Optional[Sequence[Any]] = None) -> None:
    pool = _get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, _adapt_params(params))
            conn.commit()


def db_fetchall(query: str, params: Optional[Sequence[Any]] = None) -> list[dict]:
    pool = _get_pool()
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(query, _adapt_params(params))
            results = list(cur.fetchall())
            return [_convert_types(r) for r in results]


def db_fetchone(query: str, params: Optional[Sequence[Any]] = None) -> Optional[dict]:
    pool = _get_pool()
    with pool.connection() as conn:
        conn.row_factory = dict_row
        with conn.cursor() as cur:
            cur.execute(query, _adapt_params(params))
            row = cur.fetchone()
            return _convert_types(dict(row)) if row else None


def _adapt_params(params: Optional[Sequence[Any]]) -> Optional[Sequence[Any]]:
    if params is None:
        return None
    adapted = []
    for value in params:
        if isinstance(value, (dict, list)):
            adapted.append(Json(value))
        else:
            adapted.append(value)
    return tuple(adapted)


def _convert_types(row: dict) -> dict:
    """Convert UUID and other non-JSON types to strings."""
    from uuid import UUID
    result = {}
    for key, value in row.items():
        if isinstance(value, UUID):
            result[key] = str(value)
        elif isinstance(value, (dict, list)):
            result[key] = value
        else:
            result[key] = value
    return result
