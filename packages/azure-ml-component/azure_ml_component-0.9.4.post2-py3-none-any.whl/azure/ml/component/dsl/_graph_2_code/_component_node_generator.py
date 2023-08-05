# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from pydash import get

from azure.ml.component._restclients.service_caller_factory import _DesignerServiceCallerFactory
from azure.ml.component.dsl._graph_2_code._base_generator import CodeBaseGenerator
from azure.ml.component.dsl._graph_2_code._utils import (
    GraphUtil, _is_pipeline_component, COMPONENT_NODE_TEMPLATE, GraphStructureError, _equal_to_enum_val,
    _get_string_concatenate_val, _normalize_param_val, process_error, _normalize_string_param_val, DataUtil,
    _convert_column_picker_val
)
from azure.ml.component._core import ComponentType
from azure.ml.component._restclients.designer.models import (
    GraphModuleNode, ParameterValueType,
    ModuleRunSettingTypes, RunSettingUIWidgetTypeEnum, OutputSetting,
    UIWidgetTypeEnum, ParameterType, RunSettingParameterType, DataStoreMode
)
from azure.ml.component._util._utils import _get_enum

_target_selector_name_2_def = {}


def _get_target_selector_type(job_type, name):
    # target selector type is not stored in pipeline graph, currently we use an extra call to get it
    # TODO(1549995): change to get from graph when backend supports
    run_setting_definitions = _DesignerServiceCallerFactory.get_instance(
        None).get_component_run_setting_parameters_mapping().get(job_type)
    if not _target_selector_name_2_def:
        for run_def in run_setting_definitions:
            if run_def.name in ComponentCodeGenerator.TARGET_SELECTOR_ARG_NAME_MAPPING.keys():
                _target_selector_name_2_def[run_def.name] = run_def
    if name in _target_selector_name_2_def.keys():
        return _target_selector_name_2_def[name].parameter_type
    else:
        return RunSettingParameterType.string


class ComponentCodeGenerator(CodeBaseGenerator):
    TARGET_SELECTOR = "Target selector"
    TARGET_SELECTOR_ARG_NAME_MAPPING = {
        TARGET_SELECTOR + " Compute type": "compute_type",
        TARGET_SELECTOR + " Instance type": "instance_type",
        TARGET_SELECTOR + " Instance types": "instance_types",
        TARGET_SELECTOR + " Region": "region",
        TARGET_SELECTOR + " My resource only": "my_resource_only",
        TARGET_SELECTOR + " Allow spot vm": "allow_spot_vm"
    }
    ROOT_RUN_SETTING_KEY = "root"
    ENVIRONMENT_VAR_RUN_SETTING_NAME = "Environment variables"

    def __init__(
            self,
            node: GraphModuleNode,
            util: GraphUtil,
            **kwargs
    ):
        super(ComponentCodeGenerator, self).__init__(**kwargs)
        self._node = node
        self.util = util
        self._definition = util.node_id_2_module[node.id]
        self.is_pipeline_component = _is_pipeline_component(self._definition)
        self._node_name = self.util.node_id_2_var_name[self._node.id]
        self._component_func_name = self.util.module_id_2_func_name[self._node.module_id]
        # dict from param name to param value
        self._params = self._get_params()
        self._run_settings, self._k8s_run_settings = self._get_run_settings()
        self._inputs_configure = self._get_inputs_configure()
        self._outputs_configure, self._register_as_dict = self._get_outputs_configure()

    @property
    def tpl_file(self):
        return COMPONENT_NODE_TEMPLATE

    @property
    def entry_template_keys(self):
        return [
            "node_name",
            "component_func_name",
            "params",
            "run_settings",
            "k8s_run_settings",
            "regenerate_output",
            "inputs_configure",
            "outputs_configure",
            "register_as"
        ]

    @property
    def node_name(self):
        return self._node_name

    @property
    def component_func_name(self):
        return self._component_func_name

    @property
    def params(self):
        return self._params

    @property
    def run_settings(self):
        return self._run_settings

    @property
    def k8s_run_settings(self):
        return self._k8s_run_settings

    @property
    def inputs_configure(self):
        return self._inputs_configure

    @property
    def outputs_configure(self):
        return self._outputs_configure

    @property
    def regenerate_output(self):
        return self._node.regenerate_output

    @property
    def register_as(self):
        return self._register_as_dict

    def _get_params(self):
        params_dict = {}
        # find inputs
        inputs = self.util.get_all_input_edges_to_node(self._node.id)
        for port in inputs:
            var_name = self.util.get_input_port_arg_name(port.destination_input_port)
            graph_port_name = port.source_output_port.graph_port_name
            node_id = port.source_output_port.node_id

            if graph_port_name:
                # pipeline input parameter for sub pipeline
                val = self.util.pipeline_param_2_py_name[graph_port_name]
            elif self.util.node_id_2_data.get(node_id):
                # dataset node
                val = self.util.get_data_node_arg_val(node_id)
            elif self.util.node_id_2_module.get(node_id):
                # output of another node
                output_name = self.util.get_output_port_arg_name(port.source_output_port)
                val = f"{self.util.node_id_2_var_name[node_id]}.outputs.{output_name}"
            else:
                raise GraphStructureError(f"Input {port} to node {self._node} not found.")
            params_dict[var_name] = val

        # find parameters
        parameters = self._node.module_parameters
        non_run_setting_params = {p.name: p for p in self._definition.module_entity.structured_interface.parameters}
        if parameters:
            for param in parameters:
                if param.name not in non_run_setting_params.keys():
                    # filter run setting parameters
                    continue
                param_name = self.util.get_param_argument_name(self._node.id, param.name)
                if _equal_to_enum_val(param.value_type, ParameterValueType.graph_parameter_name):
                    # pipeline parameter
                    val = self.util.pipeline_param_2_py_name[param.value]
                elif _equal_to_enum_val(param.value_type, ParameterValueType.concatenate):
                    # string concatenate
                    val = _get_string_concatenate_val(param.assignments_to_concatenate)
                else:
                    val = param.value
                    param_def = non_run_setting_params[param.name]
                    # skip generate parameters with default value
                    if val == param_def.default_value:
                        continue
                    param_type = _get_enum(param_def.parameter_type, ParameterType) or ParameterType.string
                    if param_def.ui_hint and _equal_to_enum_val(
                            param_def.ui_hint.ui_widget_type, UIWidgetTypeEnum.column_picker):
                        # handle column picker val
                        val = _convert_column_picker_val(val)
                    if (self._definition.job_type == ComponentType.SweepComponent.value) and (
                            param_name == "model" and val):
                        # hard code logic to handle sweep component model parameter
                        # just use the original val as a dict
                        pass
                    else:
                        val = _normalize_param_val(val, param_type)
                params_dict[param_name] = val

        return params_dict

    def _get_run_settings(self):
        # Mapping in format: {section_name: {argument_name: val}}
        settings = {}
        compute_settings = {}
        run_setting_node = self.util.node_id_2_run_setting.get(self._node.id)

        def add_setting(settings_dict, section_name, arg_name, val):
            # use root as key for top level run settings
            if section_name is None:
                section_name = self.ROOT_RUN_SETTING_KEY
            if not arg_name:
                process_error(GraphStructureError("Missing arg name."))
                return
            if section_name not in settings_dict:
                settings_dict[section_name] = {}
            settings_dict[section_name][arg_name] = val

        if run_setting_node and run_setting_node.run_settings:
            run_setting_def = self.util.node_id_2_run_setting_def[self._node.id]
            name_to_def = {s.name: s for s in run_setting_def}
            for setting in run_setting_node.run_settings:
                # the run setting is set by a linked module parameter, no need to parse here
                if setting.linked_parameter_name:
                    continue
                # hard code to determine if environment_variables is default value
                # TODO: normalize the way to determine if a run setting is using default value
                if setting.name == self.ENVIRONMENT_VAR_RUN_SETTING_NAME and setting.value == "{}":
                    continue
                if setting.name not in name_to_def.keys():
                    # ignore legacy run settings which don't have definition, eg: Priority
                    continue
                setting_def = name_to_def[setting.name]
                # filter out legacy run setting
                if _equal_to_enum_val(setting_def.module_run_setting_type, ModuleRunSettingTypes.legacy):
                    continue

                # for run settings without argument name, it's not supported by SDK, eg: 'BanditSlackSettingValue'
                if not setting_def.argument_name:
                    continue

                # TODO: too much indents, refactor, move out?
                if setting_def.run_setting_ui_hint and _equal_to_enum_val(
                        setting_def.run_setting_ui_hint.ui_widget_type, RunSettingUIWidgetTypeEnum.compute_selection):
                    # compute run setting
                    if not setting.use_graph_default_compute:
                        # handle target selector
                        if setting.value is None and setting.mlc_compute_type:
                            # in this case, the compute is set through target selector
                            for _s in run_setting_node.run_settings:
                                if _s.name in self.TARGET_SELECTOR_ARG_NAME_MAPPING.keys():
                                    target_selector_name = self.TARGET_SELECTOR_ARG_NAME_MAPPING[_s.name]
                                    target_selector_type = _get_target_selector_type(
                                        self._definition.module_entity.step_type, _s.name)
                                    val = _normalize_param_val(
                                        _s.value, _get_enum(target_selector_type, RunSettingParameterType))
                                    add_setting(settings, "target_selector", target_selector_name, val)
                        elif setting.value:
                            val = _normalize_string_param_val(setting.value)
                            add_setting(settings, setting_def.section_argument_name, setting_def.argument_name, val)

                    # handle k8s run setting
                    if setting.compute_run_settings:
                        compute_type = setting.mlc_compute_type
                        _m = setting_def.run_setting_ui_hint.compute_selection.compute_run_settings_mapping
                        compute_defs = _m.get(compute_type, [])
                        if not compute_defs:
                            self.logger.warning(f"No setting parameters found for computeType: {compute_type}")
                        for param_def in compute_defs:
                            param_type = param_def.parameter_type
                            compute_setting = next(
                                (s for s in setting.compute_run_settings if s.name == param_def.name), None)
                            if not compute_setting:
                                continue
                            val = _normalize_param_val(
                                compute_setting.value, _get_enum(param_type, RunSettingParameterType))
                            add_setting(
                                compute_settings, param_def.section_argument_name, param_def.argument_name, val)

                elif setting.value:
                    # skip generate run settings with default value
                    if setting.value == setting_def.default_value:
                        continue
                    val = _normalize_param_val(
                        setting.value, _get_enum(setting_def.parameter_type, RunSettingParameterType))
                    # Currently all run settings' depth is at most 2, when there are settings depth > 3,
                    # eg: run_settings.a.b.c = val, we need to make sure section_argument_name for c is a.b,
                    # or we need to recursively find section_argument_name for c
                    add_setting(settings, setting_def.section_argument_name, setting_def.argument_name, val)
        return settings, compute_settings

    def _get_input_output_settings(self, settings, io_definitions, python_interface):
        io_config = {}
        register_config = {}
        for setting in settings:
            setting_dict = {}
            definition = next((i for i in io_definitions if i.name == setting.name), None)
            if not definition:
                process_error(GraphStructureError(f"Failed to find definition for input/output setting {setting}"))
            argument_name = next((a.argument_name for a in python_interface if a.name == setting.name), None)
            if not argument_name:
                continue
            # input output shared fields
            # data store mode in settings and in definition are not the same class
            if not _equal_to_enum_val(setting.data_store_mode, DataStoreMode.none) and (
                    setting.data_store_mode != definition.data_store_mode):
                mode = _get_enum(setting.data_store_mode, DataStoreMode).name
                setting_dict["mode"] = _normalize_string_param_val(mode)
            if setting.path_on_compute:
                setting_dict["path_on_compute"] = _normalize_string_param_val(setting.path_on_compute)
            # output only fields
            if isinstance(setting, OutputSetting):
                if not self.util.is_default_datastore(setting.data_store_name, definition):
                    self.util.used_datastore = True
                    data_store_val = f"Datastore({self.util.workspace_name}, {repr(setting.data_store_name)})"
                    setting_dict["datastore"] = data_store_val
                if setting.dataset_output_options and setting.dataset_output_options.path_on_datastore and (
                        setting.dataset_output_options.path_on_datastore != DataUtil.LEGACY_DATA_REFERENCE_FORMAT):
                    path_on_datastore = setting.dataset_output_options.path_on_datastore
                    setting_dict["path_on_datastore"] = _normalize_string_param_val(path_on_datastore)
                # get register as dict
                # Register as can not set in configure, use self._register_as_dict to represent
                if setting.dataset_registration and setting.dataset_registration.name:
                    register_as_dict = {
                        "name": repr(setting.dataset_registration.name)
                    }
                    if setting.dataset_registration.create_new_version:
                        register_as_dict["create_new_version"] = True
                    if setting.dataset_registration.tags:
                        register_as_dict["tags"] = setting.dataset_registration.tags
                    if setting.dataset_registration.description:
                        register_as_dict["description"] = setting.dataset_registration.description
                    register_config[argument_name] = register_as_dict
            if setting_dict:
                io_config[argument_name] = setting_dict
        return io_config, register_config

    def _get_inputs_configure(self):
        """Returns input configure, eg: {"input_name": {"mode": xxx, "path_on_compute": xxx}}
        which will be translate to node.inputs.input1.configure(mode="", path_on_compute="").
        """
        # TODO: input configure for pipeline component
        if self.is_pipeline_component:
            return {}
        return self._get_input_output_settings(
            self._node.module_input_settings,
            self._definition.module_entity.structured_interface.inputs,
            get(self._definition, "module_python_interface.inputs", []),
        )[0]

    def _get_outputs_configure(self):
        """Returns tuple of output configure and register as configure.
        eg: {"output1": {"mode": xxx, "path_on_compute": xxx}},
            {"output1": {"name": xxx, "create_new_version": xxx}}
        which will be translate to node.outputs.output1.configure(mode="", path_on_compute="").
        which will be translate to node.outputs.output1.register_as(name="", create_new_version="").
        """
        if self.is_pipeline_component:
            return {}, {}
        return self._get_input_output_settings(
            self._node.module_output_settings,
            self._definition.module_entity.structured_interface.outputs,
            get(self._definition, "module_python_interface.outputs", []),
        )
