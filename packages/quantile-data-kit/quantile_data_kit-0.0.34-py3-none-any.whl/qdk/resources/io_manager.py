import os

from dagster import Bool, Field, IOManager, OutputContext, StringSource, check
from dagster import io_manager as dagster_io_manager
from dagster.core.storage.fs_io_manager import PickledObjectFilesystemIOManager
from qdk.materialization import Materializer


class IOManager(IOManager):
    def __init__(self):
        self.values = {}

    def handle_output(self, context: OutputContext, obj):
        keys = context.get_output_identifier()
        self.values[tuple(keys)] = obj

        # Create a materializer for the object
        asset_materialization = Materializer(context, obj).materialize()

        # If the asset was materialized, yield the asset
        if asset_materialization:
            yield asset_materialization

    def load_input(self, context):
        keys = tuple(context.upstream_output.get_output_identifier())

        if keys not in self.values:
            raise KeyError(
                "The key was not found. Make sure the io_manager lives between execution processes."
            )

        obj = self.values[keys]
        return obj


class FilesystemIOManager(PickledObjectFilesystemIOManager):
    def __init__(self, base_dir=None, store_runs=False):
        super().__init__(base_dir=base_dir)
        self.store_runs = check.bool_param(store_runs, "store_runs")

    def _get_path(self, context: OutputContext):
        """Automatically construct filepath."""
        keys = context.get_output_identifier()

        # If not storing individual runs
        # replace the run id with the pipeline name
        if not self.store_runs:
            keys = [context.pipeline_name] + keys[1:]

        return os.path.join(self.base_dir, *keys)

    def handle_output(self, context: OutputContext, obj):
        """
        Pickle the data and store the object to a file.
        We added custom functionality to materialize the asset.
        """
        # Use the inherited handle_output to store the object
        super().handle_output(context, obj)

        # Create a materializer for the object
        asset_materialization = Materializer(context, obj).materialize()

        # If the asset was materialized, yield the asset
        if asset_materialization:
            yield asset_materialization


@dagster_io_manager
def qdk_io_manager(_):
    return IOManager()


@dagster_io_manager(
    config_schema={
        "base_dir": Field(StringSource, is_required=False),
        "store_runs": Field(
            Bool,
            default_value=False,
            description="Whether to create seperate directories for each individual run.",
        ),
    }
)
def qdk_fs_io_manager(init_context):
    base_dir = init_context.resource_config.get(
        "base_dir", init_context.instance.storage_directory()
    )
    store_runs = init_context.resource_config.get("store_runs")
    return FilesystemIOManager(base_dir, store_runs)
