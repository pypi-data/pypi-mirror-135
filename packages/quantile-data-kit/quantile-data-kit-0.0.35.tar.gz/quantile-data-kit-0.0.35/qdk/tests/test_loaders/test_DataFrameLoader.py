from dagster import OpDefinition
from dask.dataframe import DataFrame as DaskDataFrame
from pandas import DataFrame
from qdk import DataFrameLoader, DataFrameType

from ..utils.dataframe import (
    CSVStoreDataFrame,
    JSONStoreDataFrame,
    PickleStoreDataFrame,
    StoreDataFrame,
)


def test_compute_ddf(tmpdir):
    """Test computer_dff parameter of DataFrameLoader.

    Args:
        tmpdir (str): The path to the temporary directory created by pytest
    """
    df_storer = CSVStoreDataFrame()
    df_path = df_storer.store_dataframe(tmpdir)

    lazy_ddf = DataFrameLoader.load(df_path, use_dask=True)
    computed_ddf = DataFrameLoader.load(df_path, use_dask=True, compute_ddf=True)

    assert isinstance(lazy_ddf, DaskDataFrame)
    assert isinstance(computed_ddf, DataFrame)


def test_csv_loading(tmpdir):
    """Test loading a csv file.

    Args:
        tmpdir (str): The path to the temporary directory created by pytest
    """
    df_storer = CSVStoreDataFrame()
    df_path = df_storer.store_dataframe(tmpdir)

    loaded_df = DataFrameLoader.load(df_path)
    loaded_ddf = DataFrameLoader.load(df_path, use_dask=True).compute()

    assert loaded_df.equals(df_storer.df)
    assert loaded_ddf.equals(df_storer.df)


def test_json_loading(tmpdir):
    """Test loading a json file.

    Args:
        tmpdir (str): The path to the temporary directory created by pytest
    """
    df_storer = JSONStoreDataFrame()
    df_path = df_storer.store_dataframe(tmpdir)

    loaded_df = DataFrameLoader.load(df_path)
    loaded_ddf = DataFrameLoader.load(df_path, use_dask=True).compute()

    assert loaded_df.equals(df_storer.df)
    assert loaded_ddf.equals(df_storer.df)


def test_pickle_loading(tmpdir):
    """Test loading a pickle file.

    Args:
        tmpdir (str): The path to the temporary directory created by pytest
    """
    df_storer = PickleStoreDataFrame()
    df_path = df_storer.store_dataframe(tmpdir)

    loaded_df = DataFrameLoader.load(df_path)
    loaded_ddf = DataFrameLoader.load(df_path, use_dask=True, repartitions=1).compute()

    assert loaded_df.equals(df_storer.df)
    assert loaded_ddf.equals(df_storer.df)


def test_op_creation():
    df_loader = DataFrameLoader
    op = df_loader.to_op("df_loader")

    assert type(op) == OpDefinition


def test_dagster_output_def():
    df_loader = DataFrameLoader
    op = df_loader.to_op("df_loader")

    assert len(op.output_defs) == 1
    assert op.output_defs[0].dagster_type == DataFrameType
