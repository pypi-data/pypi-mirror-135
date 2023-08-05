# Stubs for galaxy.tools.verify.test_data (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

UPDATE_TEMPLATE = ...  # type: Any
UPDATE_FAILED_TEMPLATE = ...  # type: Any
LIST_SEP = ...  # type: Any

class TestDataResolver:
    resolvers = ...  # type: Any
    def __init__(self, env_var: str = ..., environ: Any = ...) -> None: ...
    def get_filename(self, name): ...

def build_resolver(uri, environ): ...

class FileDataResolver:
    file_dir = ...  # type: Any
    def __init__(self, file_dir) -> None: ...
    def exists(self, filename): ...
    def path(self, filename): ...

class GitDataResolver(FileDataResolver):
    repository = ...  # type: Any
    updated = ...  # type: bool
    fetch_data = ...  # type: Any
    def __init__(self, repository, environ) -> None: ...
    def exists(self, filename): ...
    def update_repository(self): ...
    def execute(self, cmd): ...
