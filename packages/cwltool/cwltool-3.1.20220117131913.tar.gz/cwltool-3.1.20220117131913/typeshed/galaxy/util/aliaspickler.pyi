# Stubs for galaxy.util.aliaspickler (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
import pickle
from six.moves import cStringIO as StringIO

class AliasUnpickler(pickle.Unpickler):
    aliases = ...  # type: Any
    def __init__(self, aliases, *args, **kw) -> None: ...
    def find_class(self, module, name): ...

class AliasPickleModule:
    aliases = ...  # type: Any
    def __init__(self, aliases) -> None: ...
    def dump(self, obj, fileobj, protocol: int = ...): ...
    def dumps(self, obj, protocol: int = ...): ...
    def load(self, fileobj): ...
    def loads(self, string): ...
