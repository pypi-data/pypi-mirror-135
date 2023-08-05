# Stubs for networkx.algorithms.connectivity.disjoint_paths (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from networkx.algorithms.flow import edmonds_karp
from typing import Any, Optional

default_flow_func = edmonds_karp

def edge_disjoint_paths(G, s, t, flow_func: Optional[Any] = ..., cutoff: Optional[Any] = ..., auxiliary: Optional[Any] = ..., residual: Optional[Any] = ...): ...
def node_disjoint_paths(G, s, t, flow_func: Optional[Any] = ..., cutoff: Optional[Any] = ..., auxiliary: Optional[Any] = ..., residual: Optional[Any] = ...): ...
