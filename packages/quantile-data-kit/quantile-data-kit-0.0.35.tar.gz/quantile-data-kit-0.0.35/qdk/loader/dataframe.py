from typing import Any, Dict, List, Optional, Union

import dask.dataframe as dd
import pandas as pd
from dagster import Field, Noneable, OutputDefinition, Permissive
from qdk.dagster_types import DataFrameType
from qdk.loader.base import BaseLoader
from qdk.s3_connection import S3Connection


class DataFrameLoader(BaseLoader):
    output_defs = [
        OutputDefinition(DataFrameType, "df"),
    ]

    config_schema = {
        "uri": Field(
            str,
            description="The uri to load the dataframe from.",
        ),
        "use_dask": Field(
            bool,
            default_value=False,
            description="Whether to load the dataframe using Dask.",
        ),
        "repartitions": Field(
            int,
            is_required=False,
            description="How many partitions to create.",
        ),
        "drop_na": Field(
            Noneable([str]),
            default_value=None,
            description="Whether to drop rows with missing values. ('column', or ['col_a', 'col_b'])",
        ),
        "drop_duplicates": Field(
            Noneable([str]),
            default_value=None,
            description="Whether to drop duplicates in certain columns. ('column', or ['col_a', 'col_b'])",
        ),
        "compute_ddf": Field(
            bool,
            default_value=False,
            description="Whether to compute the dask dataframe.",
        ),
        "load_params": Field(
            Permissive({}),
            description="Extra parameters that get passed to the loading function.",
        ),
    }

    @staticmethod
    def post_process(
        df: Union[pd.DataFrame, dd.DataFrame],
        drop_na: List[str],
        drop_duplicates: List[str],
        compute_ddf: bool,
    ):
        """
        This function post processes the dataframe after loading
        the data.
        """
        if drop_na:
            df = df.dropna(subset=drop_na)

        if drop_duplicates:
            df = df.drop_duplicates(subset=drop_duplicates)

        if compute_ddf:
            df = df.compute()

        return df

    @classmethod
    def load(
        cls,
        uri: str,
        use_dask: bool = False,
        repartitions: int = None,
        drop_na: List[str] = None,
        drop_duplicates: List[str] = None,
        compute_ddf: bool = False,
        load_params: Dict[str, Any] = {},
    ) -> Union[pd.DataFrame, dd.DataFrame]:
        # Choose which framework to use for loading the data
        framework = dd if use_dask else pd

        # Inject S3 connection information into the load parameters
        # if the uri starts with an S3 connection indicator
        if uri.startswith("s3://"):
            s3_connection = S3Connection()
            load_params = {
                "storage_options": {
                    "client_kwargs": {
                        "aws_access_key_id": s3_connection.aws_access_key_id,
                        "aws_secret_access_key": s3_connection.aws_access_secret_key,
                        "endpoint_url": s3_connection.aws_endpoint_url,
                    }
                },
                **load_params,
            }

        if uri.endswith(".csv"):
            df = framework.read_csv(
                uri,
                **load_params,
            )

        if uri.endswith(".parquet"):
            df = framework.read_parquet(
                uri,
                **load_params,
            )

        elif (
            uri.endswith(".json")
            or uri.endswith(".jsonl")
            or uri.endswith(".jsonlines")
        ):
            df = framework.read_json(
                uri,
                orient="records",
                lines=True,
                **load_params,
            )

        elif uri.endswith(".pkl"):
            df = pd.read_pickle(
                uri,
                **load_params,
            )

            if use_dask:
                df = dd.from_pandas(
                    df,
                    npartitions=repartitions,
                )

        # Post process the data that is coming in
        df = cls.post_process(
            df,
            drop_na=drop_na,
            drop_duplicates=drop_duplicates,
            compute_ddf=compute_ddf,
        )

        return df
