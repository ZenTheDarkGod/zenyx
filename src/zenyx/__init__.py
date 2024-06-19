"""
# zenyx
version 1.0.1\n

## pyon (python obejct notation)
Enables convertion from objects into JSON and back. 
Just use the common JSON functions such as:
 - `dump`: save an `object`, a `dict` or a `list` into a `.json` file
 - `load`: load an `object`, a `dict` or a `list` from a `.json` file
 - `dumps`: convert an `object`, a `dict` or a `list` into a JSON object (string)
 - `loads`: convert a JSON object (string) into an `object`, a `dict` or a `list`

## object streaming
Watcher: reload object array on json file change. 
Enables the continous loading of a json file.\n
Implemented in: `object_stream`

## require
Runtime import and/or install of modules
Implemented in: `require`

## printf
A better printing solution which naturally contains bold (`@!`), italic (`@?`), dark (`@~`) and underlined (`@_`) text \n
Includes the reset (`$&`) symbol \n
### Other Capabilities:
- `printf.full_line(<args>, <kwargs>)` -> Prints a whole line with `content + " "*remaining_line_length`
- `printf.endl(<amount = 0>)` -> An easy way to print multiple `\n`s
- `printf.title(<content>, <line_char>)` -> Prints the title to the middle of the console using the line_char as the spacing chartacter
"""

from dataclasses import dataclass
from typing import *
import inspect
import copy
import sys

from . import pyon, require, streams
from .console import printf
from .args import Arguments
from .pipe import Pipe


T = TypeVar("T")
K = TypeVar("K")


def unreachable(msg: str) -> Never:
    stack = inspect.stack()[1]
    printf(
        "\n\n@!unreachable$&"
        + f"\n@~In {stack.filename}, line {stack.lineno} in {stack.function}()$&"
    )
    printf(f"\n@!Error Message:$&\n{msg}")
    raise Exception("unreachable")


class DummyFile:
    def write(self, x):
        pass

    def flush(self, x=None):
        pass


def silence(func: Callable):
    def wrap(*args, **kwargs):
        res, exc = None, None
        save_stdout = sys.stdout
        sys.stdout = DummyFile()
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            exc = e
        sys.stdout = save_stdout
        if exc:
            raise exc
        return res

    return wrap


def struct(cls: object.__class__):
    for attr, Type in inspect.getmembers(cls):
        if Type.__class__.__name__ == "function":
            delattr(cls, attr)

    return dataclass(cls)


def clone(a: T) -> T:
    return copy.copy(a)


def structured_clone(a: T) -> T:
    return copy.deepcopy(a)


def weak_cast(Type: T, a: Any) -> T:
    return a