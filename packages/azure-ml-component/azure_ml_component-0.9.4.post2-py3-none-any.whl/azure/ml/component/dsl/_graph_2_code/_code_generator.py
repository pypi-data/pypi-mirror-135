# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import argparse
import logging
import sys
from pathlib import Path

from azureml.core import Workspace, Run, Experiment
from azureml._common.async_utils import TaskQueue
from azure.ml.component._graph_to_code import _parse_designer_url
from azure.ml.component.dsl._graph_2_code._base_generator import CodeBaseGenerator
from azure.ml.component.dsl._graph_2_code._file_header_generator import CodeFileHeaderGenerator
from azure.ml.component.dsl._graph_2_code._pipeline_generator import PipelineCodeGenerator
from azure.ml.component.dsl._graph_2_code._utils import INIT_TEMPLATE, RUN_TEMPLATE, GraphPackageUtil, \
    _is_anonymous_pipeline_component, NOTE_BOOK_TEMPLATE
from azure.ml.component._util._loggerfactory import _LoggerFactory, _PUBLIC_API, track
from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component._restclients.designer.models import PipelineGraph
from azure.ml.component.dsl._component_generator import GraphComponentSnapshotGenerator
from azure.ml.component.dsl._utils import logger, _log_without_dash
from azure.ml.component._util._utils import (
    _sanitize_python_variable_name, TimerContext, environment_variable_overwrite
)
from azure.ml.component._api._snapshots_client import AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR

_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger
    _logger = _LoggerFactory.get_logger("az-ml")
    return _logger


class PipelinePackageInit(CodeBaseGenerator):
    def __init__(self, graph_generators, **kwargs):
        super(PipelinePackageInit, self).__init__(**kwargs)
        self.module_2_func = {g.module_name: g.pipeline_func_name for g in graph_generators}
        self.target_file = "__init__.py"

    @property
    def tpl_file(self):
        return INIT_TEMPLATE

    @property
    def entry_template_keys(self):
        return {
            "module_2_func": self.module_2_func
        }


class RunScript(CodeBaseGenerator):
    DEFAULT_EXPERIMENT_NAME = "sample-experiment-name"
    TARGET_FILE = "run.py"

    def __init__(self, root_pipeline_generator: PipelineCodeGenerator, header=None, run=None):
        super(RunScript, self).__init__(target_file=self.TARGET_FILE)
        self.pipeline_module_name = root_pipeline_generator.module_name
        self._header = header if header else CodeFileHeaderGenerator().to_component_entry_code()
        self._experiment_name = self.DEFAULT_EXPERIMENT_NAME if not run else run.experiment.name

    @property
    def header(self):
        return self._header

    @property
    def pipeline_submit_params(self):
        submit_params = {"workspace": "workspace", "experiment_name": repr(self._experiment_name)}
        return [f"{name}={val}" for name, val in submit_params.items()]

    @property
    def entry_template_keys(self):
        return [
            "header",
            "pipeline_module_name",
            "pipeline_submit_params"
        ]

    @property
    def tpl_file(self):
        return RUN_TEMPLATE


class NotebookGenerator(CodeBaseGenerator):
    DEFAULT_EXPERIMENT_NAME = "sample-experiment-name"
    TARGET_FILE = "run.ipynb"

    def __init__(self, root_pipeline_generator: PipelineCodeGenerator, url=None, run=None):
        super(NotebookGenerator, self).__init__(target_file=self.TARGET_FILE)
        self.pipeline_module_name = root_pipeline_generator.module_name
        self._url = url if url else CodeFileHeaderGenerator.DEFAULT_URL
        self._experiment_name = self.DEFAULT_EXPERIMENT_NAME if not run else run.experiment.name

    @property
    def url(self):
        return self._url

    @property
    def pipeline_submit_params(self):
        submit_params = {"workspace": "workspace", "experiment_name": repr(self._experiment_name)}
        return ", ".join(f"{key}={val}" for key, val in submit_params.items())

    @property
    def tpl_file(self):
        return NOTE_BOOK_TEMPLATE

    @property
    def entry_template_keys(self):
        # use entry_template_key_val here to customize template keys
        return []

    @property
    def entry_template_key_val(self):
        return {
            "{url}": self.url,
            "{pipeline_module_name}": self.pipeline_module_name,
            "{pipeline_submit_params}": self.pipeline_submit_params
        }

    def to_component_entry_code(self):
        with open(self.tpl_file) as f:
            result = f.read()
        # use str replace here since notebook need a lot of escape using template
        for key, val in self.entry_template_key_val.items():
            result = result.replace(key, val)
        return result


class PipelinePackageGenerator:

    def __init__(self, workspace, run_id, include_components: str = None, target_dir=None):
        self.service_caller = _DesignerServiceCallerFactory.get_instance(workspace)
        root_pipeline = self.service_caller.get_pipeline_run(run_id)
        experiment_name = root_pipeline.experiment_name
        experiment = Experiment(workspace=workspace, name=experiment_name)
        root_run = Run(experiment, run_id=run_id)
        url = root_run.get_portal_url()
        self._file_header_generator = CodeFileHeaderGenerator(url=url)
        file_header = self._file_header_generator.to_component_entry_code()
        # Use experiment name + display name to uniquely define a pipeline
        self.run_identifier = _sanitize_python_variable_name(f"{experiment_name}_{root_run.display_name}")
        if not target_dir:
            target_dir = self.run_identifier
        self.workspace = workspace
        self.target_dir = Path(target_dir)
        self.logger = logging.getLogger(self.__class__.__name__)
        # Mapping from graph id to graph entity
        self.graph_id_2_entity = {}
        # Mapping from graph id to definition
        self.graph_id_2_definition = {}
        root_graph = self.service_caller.get_pipeline_run_graph_no_status(
            pipeline_run_id=run_id, has_namespace_concept=False)
        self._get_graphs_for_anonymous_pipeline_components(root_graph)
        self.graphs = list(self.graph_id_2_entity.values())
        self.graphs.append(root_graph)
        self.pkg_util = GraphPackageUtil(self.graphs, include_components=include_components)
        self._components_dir = self.target_dir / self.pkg_util.COMPONENT_PACKAGE_NAME
        self._pipelines_dir = self.target_dir / self.pkg_util.PIPELINE_PACKAGE_NAME
        self._sub_pipeline_dir = self._pipelines_dir / self.pkg_util.SUBGRAPH_PACKAGE_NAME
        self.run_script_path = self.target_dir / RunScript.TARGET_FILE
        self._subgraph_generators = [
            PipelineCodeGenerator(
                graph, self.pkg_util,
                definition=self.graph_id_2_definition[id],
                run=root_run,
                header=file_header,
            ) for id, graph in self.graph_id_2_entity.items()
        ]
        self._root_graph_generator = PipelineCodeGenerator(
            root_graph, self.pkg_util, is_root=True, module_name=self.run_identifier, run=root_run, header=file_header
        )

        self._init_generator = PipelinePackageInit(self._subgraph_generators)
        self._run_generator = RunScript(
            root_pipeline_generator=self._root_graph_generator, header=file_header, run=root_run
        )
        self._notebook_generator = NotebookGenerator(
            root_pipeline_generator=self._root_graph_generator, url=url, run=root_run
        )

    def _get_graphs_for_anonymous_pipeline_components(self, root_graph: PipelineGraph):
        with TaskQueue(_parent_logger=self.logger) as task_queue:

            def _get_graphs_recursively(graph_id, graph_definition=None, graph=None):
                if graph is None:
                    graph = self.service_caller._get_pipeline_component_graph(graph_id=graph_id)
                    self.graph_id_2_entity[graph_id] = graph
                    self.graph_id_2_definition[graph_id] = graph_definition
                subgraph_module_ids = {n.module_id for n in graph.sub_graph_nodes}
                for dto in graph.graph_module_dtos:
                    if dto.module_version_id in subgraph_module_ids and _is_anonymous_pipeline_component(dto):
                        graph_id = dto.module_entity.cloud_settings.sub_graph_config.graph_id
                        # Note: this may run multiple time for same sub graph if they share same graph id
                        if graph_id not in self.graph_id_2_entity.keys():
                            task_queue.add(_get_graphs_recursively, graph_id, dto)

            _get_graphs_recursively(graph_id=None, graph=root_graph)
            # Note: we added tasks that will dynamically add tasks to task queue, so we need to flush task queue until
            # it has no tasks left
            while not task_queue._tasks.empty():
                task_queue.flush(source='iter_files_in_parallel')

    def generate(self):
        # TODO: raise error when target dir already exists?
        self.target_dir.mkdir(exist_ok=True)
        # generate root pipeline code
        self._pipelines_dir.mkdir(exist_ok=True)
        self._root_graph_generator.to_component_entry_file(self._pipelines_dir)
        # generate sub pipeline code
        if self._subgraph_generators:
            self._sub_pipeline_dir.mkdir(exist_ok=True)
        for g in self._subgraph_generators:
            g.to_component_entry_file(self._pipelines_dir)
        # TODO: generate package init, split root graph and sub pipelines to different classes?
        # self._init_generator.to_component_entry_file(self.target_dir)
        # generate components
        self._components_dir.mkdir(exist_ok=True)
        # Skip snapshot sas download progress bar
        with environment_variable_overwrite(AML_COMPONENT_SNAPSHOT_WITHOUT_DOWNLOAD_PROGRESS_BAR, "True"):
            GraphComponentSnapshotGenerator(
                workspace=self.workspace, target_directory=self.target_dir,
                module_name=self.pkg_util.COMPONENT_PACKAGE_NAME,
                component_id_2_func_name=self.pkg_util.generated_id_2_function,
                component_id_2_module_name=self.pkg_util.generated_id_2_module,
                snapshot_component_ids=self.pkg_util.snapshot_module_ids
            ).generate()
        # generate workspace config
        self.workspace.write_config(self.target_dir)
        # generate run script
        self._run_generator.to_component_entry_file(target_dir=self.target_dir)
        # generate notebook
        self._notebook_generator.to_component_entry_file(target_dir=self.target_dir)


def _generate_package(
        url: str = None,
        subscription_id=None, resource_group=None, workspace_name=None, run_id=None,
        include_components=None, target_dir=None
):
    if url is not None:
        subscription_id, resource_group_name, workspace_name, draft_id, run_id = _parse_designer_url(url)
    else:
        subscription_id, resource_group_name, workspace_name, draft_id, run_id = (
            subscription_id, resource_group, workspace_name, None, run_id)
    # TODO(1551983): support draft, endpoint, published pipeline
    if draft_id:
        raise NotImplementedError()
    _log_without_dash("========== Staring export pipeline code ==========")
    with TimerContext() as timer_context:
        workspace = Workspace(
            workspace_name=workspace_name, resource_group=resource_group_name,
            subscription_id=subscription_id,
        )
        generator = _generate_code(workspace, run_id, include_components, target_dir)
    logger.info(f"Generated code location: {generator.target_dir.absolute()}")
    logger.info(f"Run `python {generator.run_script_path.absolute()}` to submit the generated pipeline.")
    logger.info(f"Run `python {generator.run_script_path.absolute()} -v` to validate the generated pipeline.")
    _log_without_dash(
        f"========== Finished generate code in {timer_context.get_duration_seconds()} seconds ==========")


@track(_get_logger, activity_type=_PUBLIC_API, activity_name="graph_to_code")
def _generate_code(workspace, run_id, include_components, target_dir):
    generator = PipelinePackageGenerator(
        workspace=workspace, run_id=run_id, include_components=include_components, target_dir=target_dir)
    generator.generate()
    return generator


def _entry(argv):
    """CLI tool for component creating."""
    parser = argparse.ArgumentParser(
        prog="az-ml",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""A CLI tool to export UI graph to Component SDK code."""
    )

    subparsers = parser.add_subparsers()
    export_parser = subparsers.add_parser(
        'export',
        description='A CLI tool to export UI graph to Component SDK code.'
    )
    export_parser.add_argument(
        '--pipeline-run', type=str,
        help="ID of the Pipeline Run to export (guid)."
    )
    export_parser.add_argument(
        '--subscription_id', '-s', type=str,
        help="Subscription id."
    )
    export_parser.add_argument(
        '--resource_group', '-r', type=str,
        help="Resource group name."
    )
    export_parser.add_argument(
        '--workspace_name', '-w', type=str,
        help="Workspace name."
    )
    export_parser.add_argument(
        '--path', '-p', type=str,
        help="Path to export the pipeline to. If not specified, default be experiment name + pipeline display name."
    )
    export_parser.add_argument(
        '--url', type=str,
        help="URL of the Pipeline Run to export."
    )
    export_parser.add_argument(
        '--include-components', type=str,
        help="""Included components to download snapshot.
        * to export all components;
        ',' separated string which contains a subset of components
        """
    )
    export_parser.set_defaults(func=PipelinePackageGenerator.generate)

    args, rest_args = parser.parse_known_args(argv)
    if args.func == PipelinePackageGenerator.generate:
        _generate_package(
            url=args.url,
            subscription_id=args.subscription_id,
            resource_group=args.resource_group,
            workspace_name=args.workspace_name,
            run_id=args.pipeline_run,
            include_components=args.include_components,
            target_dir=args.path
        )


def main():
    """Use as a CLI entry function to use ComponentProject."""
    _entry(sys.argv[1:])
