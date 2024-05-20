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

from zenyx import pyon, require, streams
from zenyx.console import printf
from zenyx.args import Arguments
from zenyx.pipe import Pipe
