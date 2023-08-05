from typing import Union

import dask.dataframe as dd
import pandas as pd
from dagster import InputDefinition
from qdk.dagster_types import DataFrameType, SeriesType
from qdk.training.base import BaseTrainer

from sklearn.base import BaseEstimator


class SklearnTrainer(BaseTrainer):
    input_defs = [
        InputDefinition("X", DataFrameType),
        InputDefinition("y", SeriesType),
        InputDefinition("model", BaseEstimator),
    ]
    required_resource_keys = {"mlflow"}

    @classmethod
    def train(
        cls,
        X: Union[pd.DataFrame, dd.DataFrame],
        y: Union[pd.Series, dd.Series],
        model: BaseEstimator,
    ):
        return model.fit(X, y)
