# Stubs for coloredlogs (Python 3.7)
#
# NOTE: This dynamically typed stub was automatically generated by stubgen.

import logging
from typing import Any, Optional

WINDOWS: Any
NEED_COLORAMA = WINDOWS
DEFAULT_LOG_LEVEL: Any
DEFAULT_LOG_FORMAT: str
DEFAULT_DATE_FORMAT: str
CHROOT_FILES: Any
CAN_USE_BOLD_FONT: Any
DEFAULT_FIELD_STYLES: Any
DEFAULT_LEVEL_STYLES: Any
DEFAULT_FORMAT_STYLE: str
FORMAT_STYLE_PATTERNS: Any

def auto_install() -> None: ...
def install(level: Optional[Any] = ..., **kw: Any): ...
def check_style(value: Any): ...
def increase_verbosity() -> None: ...
def decrease_verbosity() -> None: ...
def is_verbose(): ...
def get_level(): ...
def set_level(level: Any) -> None: ...
def adjust_level(logger: Any, level: Any) -> None: ...
def find_defined_levels(): ...
def level_to_number(value: Any): ...
def find_level_aliases(): ...
def parse_encoded_styles(text: Any, normalize_key: Optional[Any] = ...): ...
def find_hostname(use_chroot: bool = ...): ...
def find_program_name(): ...
def replace_handler(logger: Any, match_handler: Any, reconfigure: Any): ...
def find_handler(logger: Any, match_handler: Any): ...
def match_stream_handler(handler: Any, streams: Any = ...): ...
def walk_propagation_tree(logger: Any) -> None: ...

class BasicFormatter(logging.Formatter):
    def formatTime(self, record: Any, datefmt: Optional[Any] = ...): ...

class ColoredFormatter(BasicFormatter):
    nn: Any = ...
    log_record_factory: Any = ...
    level_styles: Any = ...
    field_styles: Any = ...
    def __init__(self, fmt: Optional[Any] = ..., datefmt: Optional[Any] = ..., level_styles: Optional[Any] = ..., field_styles: Optional[Any] = ..., style: Any = ...) -> None: ...
    def colorize_format(self, fmt: Any, style: Any = ...): ...
    def format(self, record: Any): ...

class Empty: ...

class HostNameFilter(logging.Filter):
    @classmethod
    def install(cls, handler: Any, fmt: Optional[Any] = ..., use_chroot: bool = ..., style: Any = ...): ...
    hostname: Any = ...
    def __init__(self, use_chroot: bool = ...) -> None: ...
    def filter(self, record: Any): ...

class ProgramNameFilter(logging.Filter):
    @classmethod
    def install(cls, handler: Any, fmt: Any, programname: Optional[Any] = ..., style: Any = ...): ...
    programname: Any = ...
    def __init__(self, programname: Optional[Any] = ...) -> None: ...
    def filter(self, record: Any): ...

class StandardErrorHandler(logging.StreamHandler):
    def __init__(self, level: Any = ...) -> None: ...
    @property
    def stream(self): ...

class FormatStringParser:
    style: Any = ...
    capturing_pattern: Any = ...
    raw_pattern: Any = ...
    tokenize_pattern: Any = ...
    name_pattern: Any = ...
    def __init__(self, style: Any = ...) -> None: ...
    def contains_field(self, format_string: Any, field_name: Any): ...
    def get_field_names(self, format_string: Any): ...
    def get_grouped_pairs(self, format_string: Any): ...
    def get_pairs(self, format_string: Any) -> None: ...
    def get_pattern(self, field_name: Any): ...
    def get_tokens(self, format_string: Any): ...

class FormatStringToken: ...

class NameNormalizer:
    aliases: Any = ...
    def __init__(self) -> None: ...
    def normalize_name(self, name: Any): ...
    def normalize_keys(self, value: Any): ...
    def get(self, normalized_dict: Any, name: Any): ...
