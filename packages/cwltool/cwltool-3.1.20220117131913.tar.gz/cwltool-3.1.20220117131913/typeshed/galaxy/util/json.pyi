# Stubs for galaxy.util.json (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any, Optional

def json_fix(val): ...
def safe_dumps(*args, **kwargs): ...
def validate_jsonrpc_request(request, regular_methods, notification_methods): ...
def validate_jsonrpc_response(response, id: Optional[Any] = ...): ...
def jsonrpc_request(method, params: Optional[Any] = ..., id: Optional[Any] = ..., jsonrpc: str = ...): ...
def jsonrpc_response(request: Optional[Any] = ..., id: Optional[Any] = ..., result: Optional[Any] = ..., error: Optional[Any] = ..., jsonrpc: str = ...): ...
