# Stubs for galaxy.util.topsort (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
from galaxy.util.odict import odict as OrderedDict

class CycleError(Exception):
    preds = ...  # type: Any
    def __init__(self, sofar, numpreds, succs) -> None: ...
    def get_partial(self): ...
    def get_pred_counts(self): ...
    def get_succs(self): ...
    def get_elements(self): ...
    def get_pairlist(self): ...
    def get_preds(self): ...
    def pick_a_cycle(self): ...

def topsort(pairlist): ...
def topsort_levels(pairlist): ...
