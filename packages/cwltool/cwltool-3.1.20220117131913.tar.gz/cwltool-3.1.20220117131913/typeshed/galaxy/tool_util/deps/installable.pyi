# Stubs for galaxy.tools.deps.installable (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any

log = ...  # type: Any

class InstallableContext:
    def is_installed(self): ...
    def can_install(self): ...
    def installable_description(self): ...
    def parent_path(self): ...

def ensure_installed(installable_context, install_func, auto_init): ...
