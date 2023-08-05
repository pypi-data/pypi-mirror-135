# Stubs for networkx.algorithms.chordal (Python 3.5)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import networkx as nx
from typing import Any

class NetworkXTreewidthBoundExceeded(nx.NetworkXException): ...

def is_chordal(G): ...
def find_induced_nodes(G, s, t, treewidth_bound: Any = ...): ...
def chordal_graph_cliques(G): ...
def chordal_graph_treewidth(G): ...
