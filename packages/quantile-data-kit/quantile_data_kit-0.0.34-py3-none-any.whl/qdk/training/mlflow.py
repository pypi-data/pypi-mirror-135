from typing import Any, Dict, Union

import dask.dataframe as dd
import pandas as pd
from dagster import Field, OutputDefinition, Permissive
from qdk.dagster_types import MLFlowRunType
from qdk.mlflow import MLFlowRun
from qdk.training.base import BaseTrainer

from mlflow import autolog, set_experiment, sklearn, start_run, xgboost
from sklearn.base import BaseEstimator


class MLFlowTrainingComponent(BaseTrainer):
    output_defs = [
        OutputDefinition(MLFlowRunType, "mlflow_run"),
    ]
    config_schema = {
        "experiment_name": Field(
            str,
            default_value="default",
            description="The mlflow experiment name, if it doesn't exists it will be created.",
        )
    }

    @classmethod
    def train(
        cls,
        X: Union[pd.DataFrame, dd.DataFrame],
        y: Union[pd.Series, dd.Series],
        model: BaseEstimator,
        experiment_name: str = "default",
    ):
        set_experiment(experiment_name)
        autolog(disable=False)

        with start_run() as run:
            model.fit(X, y)

        autolog(disable=True)
        return MLFlowRun(run)
