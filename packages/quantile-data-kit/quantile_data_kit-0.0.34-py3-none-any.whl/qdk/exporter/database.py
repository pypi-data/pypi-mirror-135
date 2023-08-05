from typing import Union

import dask.dataframe as dd
import pandas as pd
from dagster import Enum, EnumValue, Field
from pandas.io.sql import SQLTable
from qdk.exporter.base import BaseExporter
from qdk.utils.sqlalchemy import create_sql_engine, get_primary_key
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.engine import Connection


class DatabaseExporter(BaseExporter):
    config_schema = {
        "database_url": Field(
            str,
            is_required=True,
            description="The sqlalchemy connection uri",
        ),
        "table_name": Field(
            str,
            is_required=True,
            description="The name of the table the data will be inserted to.",
        ),
    }

    @classmethod
    def upsert(
        cls,
        table: SQLTable,
        conn: Connection,
        keys: list,
        data_iter: zip,
    ):
        # Get the name of the primary key, used for upserting
        primary_key_name = get_primary_key(conn, table.name)

        if not primary_key_name:
            raise ValueError(
                "The table you are inserting into does not have a primary key."
            )

        upsert_args = {
            "constraint": primary_key_name,
        }

        # Loop through the data and upsert each row
        for data in data_iter:
            data = {k: data[i] for i, k in enumerate(keys)}
            upsert_args["set_"] = data
            insert_stmt = insert(cls.meta.tables[table.name]).values(**data)
            upsert_stmt = insert_stmt.on_conflict_do_update(**upsert_args)
            conn.execute(upsert_stmt)

    @classmethod
    def export(
        cls,
        df: Union[pd.DataFrame, dd.DataFrame],
        database_url: str,
        table_name: str,
    ) -> None:
        """This component uploads data to a database. You can upsert the data
        if you are using a Postgres database.

        Args:
            df (Union[pd.DataFrame, dd.DataFrame]): The dataframe you want to upload
            database_url (str): The sqlalchemy uri of the database
            table_name (str): The name of the table you want to upload to
        """
        engine, meta = create_sql_engine(database_url)

        # Bind meta to the class, because we cannot pass it
        # to the upsert function
        cls.meta = meta

        with engine.connect() as conn:
            df.to_sql(
                table_name,
                con=conn,
                if_exists="append",
                method=cls.upsert,
                index=False,
            )
