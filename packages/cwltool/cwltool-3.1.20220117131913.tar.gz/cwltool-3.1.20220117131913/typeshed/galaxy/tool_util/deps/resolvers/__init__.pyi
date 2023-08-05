# Stubs for galaxy.tools.deps.resolvers (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional
from galaxy.util.dictifiable import Dictifiable
from ..requirements import ToolRequirement as ToolRequirement

class DependencyResolver(Dictifiable):
    dict_collection_visible_keys = ...  # type: Any
    disabled = ...  # type: bool
    resolves_simple_dependencies = ...  # type: bool
    can_uninstall_dependencies = ...  # type: bool
    config_options = ...  # type: Any
    def resolve(self, requirement, **kwds): ...

class MultipleDependencyResolver:
    def resolve_all(self, requirements, **kwds): ...

class ListableDependencyResolver:
    def list_dependencies(self): ...

class MappableDependencyResolver: ...

FROM_UNVERSIONED = ...  # type: Any

class RequirementMapping:
    from_name = ...  # type: Any
    from_version = ...  # type: Any
    to_name = ...  # type: Any
    to_version = ...  # type: Any
    def __init__(self, from_name, from_version, to_name, to_version) -> None: ...
    def matches_requirement(self, requirement): ...
    def apply(self, requirement): ...
    @staticmethod
    def from_dict(raw_mapping): ...

class SpecificationAwareDependencyResolver: ...
class SpecificationPatternDependencyResolver: ...

class InstallableDependencyResolver:
    def install_dependency(self, name, version, type, **kwds): ...

class Dependency(Dictifiable):
    dict_collection_visible_keys = ...  # type: Any
    cacheable = ...  # type: bool
    def shell_commands(self, requirement): ...
    def exact(self): ...
    @property
    def resolver_msg(self): ...

class NullDependency(Dependency):
    dependency_type = ...  # type: Any
    exact = ...  # type: bool
    version = ...  # type: Any
    name = ...  # type: Any
    def __init__(self, version: Optional[Any] = ..., name: Optional[Any] = ...) -> None: ...
    @property
    def resolver_msg(self): ...
    def shell_commands(self, requirement): ...

class DependencyException(Exception): ...
