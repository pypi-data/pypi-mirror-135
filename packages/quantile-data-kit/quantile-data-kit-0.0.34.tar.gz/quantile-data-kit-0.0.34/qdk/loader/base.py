from typing import Any

from dagster import InputDefinition, Nothing, OutputDefinition
from qdk.base import BaseComponent


class BaseLoader(BaseComponent):
    compute_function = "load"
    tags = {
        "kind": "loader",
    }
    input_defs = [
        InputDefinition("after", Nothing),
    ]
    output_defs = [
        OutputDefinition(Any, "out"),
    ]

    @classmethod
    def load(cls) -> Any:
        """
        Overwrite this function to load the required object.
        """
        raise NotImplementedError(
            'Make sure you added a "load" function to the component'
        )
