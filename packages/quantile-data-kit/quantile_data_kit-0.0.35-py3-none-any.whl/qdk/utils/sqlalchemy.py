from typing import Optional, Tuple

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.sql.schema import MetaData


def create_sql_engine(database_url: str) -> Tuple[Engine, MetaData]:
    """
    Create a connection to the database using the supplied database url
    """
    engine = create_engine(database_url)
    meta = MetaData()
    meta.bind = engine
    meta.reflect(views=True)

    return (engine, meta)


def get_primary_key(conn: Connection, table_name: str) -> Optional[str]:
    primary_key = conn.execute(
        f"""
        SELECT DISTINCT tco.constraint_name
        FROM information_schema.table_constraints tco
                 JOIN information_schema.key_column_usage kcu
                      ON kcu.constraint_name = tco.constraint_name
                          AND kcu.constraint_schema = tco.constraint_schema
                          AND kcu.constraint_name = tco.constraint_name
        WHERE kcu.table_name = '{table_name}'
          AND constraint_type = 'PRIMARY KEY';
        """
    ).first()

    if primary_key:
        return primary_key[0]
    else:
        return None
