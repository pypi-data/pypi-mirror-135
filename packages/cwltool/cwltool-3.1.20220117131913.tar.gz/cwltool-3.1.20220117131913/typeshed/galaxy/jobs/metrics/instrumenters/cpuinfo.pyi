# Stubs for galaxy.jobs.metrics.instrumenters.cpuinfo (Python 3.4)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

from typing import Any
import formatting
from ..instrumenters import InstrumentPlugin

class CpuInfoFormatter(formatting.JobMetricFormatter):
    def format(self, key, value): ...

class CpuInfoPlugin(InstrumentPlugin):
    plugin_type = ...  # type: str
    formatter = ...  # type: Any
    verbose = ...  # type: Any
    def __init__(self, **kwargs) -> None: ...
    def pre_execute_instrument(self, job_directory): ...
    def job_properties(self, job_id, job_directory): ...
