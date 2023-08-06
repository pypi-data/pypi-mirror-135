from typing import Any, TypedDict

from . import Event

class Client:
    def flush(self) -> None: ...
    def new_event(self, data: dict[str, Any] = {}) -> Event: ...

class Response(TypedDict):
    status_code: int
    duration: int
    metadata: Any
    body: str
    error: str
