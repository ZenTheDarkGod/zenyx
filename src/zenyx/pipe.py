from types import UnionType
from typing import *
from typing import Any

T = TypeVar("T")
K = TypeVar("K")


class Pipe(Generic[T]):
    def __init__(self, value: T) -> None:
        self.val = value
    
    def __rshift__(self, fn: Callable[[T], K]) -> "Pipe[T]":
        self.val = fn(self.val)
        return self
    
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.val
    
