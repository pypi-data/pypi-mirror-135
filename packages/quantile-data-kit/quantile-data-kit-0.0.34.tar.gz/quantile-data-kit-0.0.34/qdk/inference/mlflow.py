from typing import Union

from dagster import InputDefinition, OutputDefinition
from dask.dataframe import DataFrame as DaskDataFrame
from dask.dataframe import Series as DaskSeries
from pandas import DataFrame, Series
from qdk.dagster_types import DataFrameType, MLFlowRunType, SeriesType
from qdk.inference.base import BaseInference
from qdk.mlflow import MLFlowRun


class MLFlowInference(BaseInference):
    compute_function = "predict"
    input_defs = [
        InputDefinition("X", DataFrameType),
        InputDefinition("mlflow_run", MLFlowRunType),
        InputDefinition("y_true", SeriesType, default_value=None),
    ]
    output_defs = [
        OutputDefinition(DataFrameType, "X_hat"),
    ]

    @classmethod
    def predict(
        cls,
        X: Union[DataFrame, DaskDataFrame],
        mlflow_run: MLFlowRun,
        y_true: Union[Series, DaskSeries] = None,
    ) -> Union[DataFrame, DaskDataFrame]:
        # Use the mlflow model to predict
        X_hat: Union[Series, DaskSeries] = mlflow_run.model.predict(X)

        X["y_hat"] = X_hat

        # If y_true is provided, add it to the output
        if y_true is not None:
            X["y_true"] = y_true

        return X
