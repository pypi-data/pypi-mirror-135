from dagster import (
    ModeDefinition,
    OpExecutionContext,
    PipelineExecutionResult,
    execute_pipeline,
    pipeline,
)
from dask.dataframe import DataFrame as DaskDataFrame
from pandas import DataFrame
from qdk import DataFrameLoader, YakeTransformer, qdk_io_manager

from ..utils.dataframe import CSVStoreDataFrame

loader_op = DataFrameLoader.to_op(
    name="loader",
)

keyword_op = YakeTransformer.to_op(
    name="keyword",
)


@pipeline(mode_defs=[ModeDefinition(resource_defs={"io_manager": qdk_io_manager})])
def nlp_pipeline():
    df = loader_op()
    keyword = keyword_op(df)


def run_pipeline(tmpdir: str, use_dask: bool) -> OpExecutionContext:
    # Create a temporary dataframe and store it in the temp directory
    df_storer = CSVStoreDataFrame()
    df_path = df_storer.store_dataframe(tmpdir)

    # Execute the pipeline
    result = execute_pipeline(
        nlp_pipeline,
        run_config={
            "ops": {
                "loader": {
                    "config": {
                        "uri": df_path,
                        "use_dask": use_dask,
                    }
                },
                "keyword": {
                    "config": {
                        "language": "en",
                        "text_columns": ["description"],
                    },
                },
            }
        },
    )

    return result


def test_nlp_pipeline(tmpdir):
    # Execute the pipeline
    result = run_pipeline(
        tmpdir,
        use_dask=False,
    )

    result_df = result.output_for_solid("keyword", "df")

    assert result.success
    assert isinstance(result, PipelineExecutionResult)
    assert isinstance(result_df, DataFrame)


def test_nlp_dask_pipeline(tmpdir):
    # Execute the pipeline
    result = run_pipeline(
        tmpdir,
        use_dask=True,
    )

    result_df = result.output_for_solid("keyword", "df")

    assert result.success
    assert isinstance(result, PipelineExecutionResult)
    assert isinstance(result_df, DaskDataFrame)
