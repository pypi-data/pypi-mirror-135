# Stubs for galaxy.tools.parser.xml (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional
from .interface import InputSource as InputSource, PageSource as PageSource, PagesSource as PagesSource, TestCollectionDef as TestCollectionDef, TestCollectionOutputDef as TestCollectionOutputDef, ToolSource as ToolSource, ToolStdioExitCode as ToolStdioExitCode, ToolStdioRegex as ToolStdioRegex
from .output_actions import ToolOutputActionGroup as ToolOutputActionGroup
from .output_collection_def import dataset_collector_descriptions_from_elem as dataset_collector_descriptions_from_elem
from .output_objects import ToolOutput as ToolOutput, ToolOutputCollection as ToolOutputCollection, ToolOutputCollectionStructure as ToolOutputCollectionStructure
from .util import aggressive_error_checks as aggressive_error_checks, error_on_exit_code as error_on_exit_code

log = ...  # type: Any

class XmlToolSource(ToolSource):
    xml_tree = ...  # type: Any
    root = ...  # type: Any
    legacy_defaults = ...  # type: Any
    def __init__(self, xml_tree, source_path: Optional[Any] = ...) -> None: ...
    def parse_version(self): ...
    def parse_id(self): ...
    def parse_tool_module(self): ...
    def parse_action_module(self): ...
    def parse_tool_type(self): ...
    def parse_name(self): ...
    def parse_edam_operations(self): ...
    def parse_edam_topics(self): ...
    def parse_description(self): ...
    def parse_is_multi_byte(self): ...
    def parse_display_interface(self, default): ...
    def parse_require_login(self, default): ...
    def parse_request_param_translation_elem(self): ...
    def parse_command(self): ...
    def parse_environment_variables(self): ...
    def parse_interpreter(self): ...
    def parse_version_command(self): ...
    def parse_version_command_interpreter(self): ...
    def parse_parallelism(self): ...
    def parse_hidden(self): ...
    def parse_redirect_url_params_elem(self): ...
    def parse_sanitize(self): ...
    def parse_refresh(self): ...
    def parse_requirements_and_containers(self): ...
    def parse_input_pages(self): ...
    def parse_outputs(self, tool): ...
    def parse_stdio(self): ...
    def parse_strict_shell(self): ...
    def parse_help(self): ...
    def parse_tests_to_dict(self): ...
    def parse_profile(self): ...

class StdioParser:
    stdio_exit_codes = ...  # type: Any
    stdio_regexes = ...  # type: Any
    def __init__(self, root) -> None: ...
    def parse_stdio_exit_codes(self, stdio_elem): ...
    def parse_stdio_regexes(self, stdio_elem): ...
    def parse_error_level(self, err_level): ...

class XmlPagesSource(PagesSource):
    input_elem = ...  # type: Any
    def __init__(self, root) -> None: ...
    @property
    def inputs_defined(self): ...

class XmlPageSource(PageSource):
    parent_elem = ...  # type: Any
    def __init__(self, parent_elem) -> None: ...
    def parse_display(self): ...
    def parse_input_sources(self): ...

class XmlInputSource(InputSource):
    input_elem = ...  # type: Any
    input_type = ...  # type: Any
    def __init__(self, input_elem) -> None: ...
    def parse_input_type(self): ...
    def elem(self): ...
    def get(self, key, value: Optional[Any] = ...): ...
    def get_bool(self, key, default): ...
    def parse_label(self): ...
    def parse_help(self): ...
    def parse_sanitizer_elem(self): ...
    def parse_validator_elems(self): ...
    def parse_dynamic_options_elem(self): ...
    def parse_static_options(self): ...
    def parse_optional(self, default: Optional[Any] = ...): ...
    def parse_conversion_tuples(self): ...
    def parse_nested_inputs_source(self): ...
    def parse_test_input_source(self): ...
    def parse_when_input_sources(self): ...
