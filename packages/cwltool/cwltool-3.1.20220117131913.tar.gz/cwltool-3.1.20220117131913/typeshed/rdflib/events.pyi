class Event:
    def __init__(self, **kw) -> None: ...

class Dispatcher:
    def set_map(self, amap): ...
    def get_map(self): ...
    def subscribe(self, event_type, handler): ...
    def dispatch(self, event) -> None: ...
