from typing import Dict, Union

import dask.dataframe as dd
import pandas as pd
from dagster import Any, InputDefinition, OutputDefinition
from qdk.base import BaseComponent


class BaseInference(BaseComponent):
    compute_function = "predict"
    tags = {
        "kind": "inference",
    }
    input_defs = [
        InputDefinition("data", pd.DataFrame),
        InputDefinition("model", Any),
    ]
    output_defs = [
        OutputDefinition(pd.DataFrame, "predictions"),
    ]

    @classmethod
    def predict(
        cls,
        df: Union[pd.DataFrame, dd.DataFrame],
        model: Any,
    ):
        raise NotImplementedError(
            'Make sure you added a "predict" function to the component'
        )
