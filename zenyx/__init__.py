"""
# zenyx
version 0.6.0\n

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
"""

from zenyx import pyon, require, streams


