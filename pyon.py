"""
# pyon
version 0.2.0\n

## python obejct notation
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

from collections import namedtuple
import json
import copy
import threading
import time
import pip


def require(package: str) -> object:
    """Implementation of Node.js's `require`. \n
    This function imports the modules at runtime, but if it cannot find them, it uses pip to install them

    Args:
        package (str): the name of the package

    Returns:
        object: the module
    """
    try:
        return __import__(package)
    except ImportError:
        pip.main(['install', package])
        return __import__(package)
    finally:
        print(f"Pakcage \"{package}\" couldn't be installed, as a resoult require couldn't import it :(")

class object_stream:
    """
    ## Constant data-streaming from a json file.\n
    This can help reduce refresh/compilation times when modifying objects.\n
    To start the `watcher` just do: 
    ```py
    x = object_stream("file.json")
    x.start()
    ```
    To stop streaming data:
    ```py
    x.stop()
    ```
    To read the objects:
    ```py
    x.get_objects()
    ```
    """
    def __init__(self, path: str, debug: bool = True, refresh_time: int = 0.25):
        self.debug = debug
        self.refresh_time = refresh_time
        self.__path = path
        self.__watch_thread = threading.Thread(target=self.__compare_and_execute)
        self.__watch_thread.setDaemon(True)
        self.__on_change_callbacks: list[callable] = []
        self.__run = True
        self.string_cache = self.__read_string_cache()
        self.__object_cache = object()
        self.__set_object_cache(self.string_cache)
        
        
    def __read_string_cache(self):
        with open(self.__path, "r") as read_file:
            return read_file.read()
    
    def __set_object_cache(self, new_cache: str):
        try:
            self.__object_cache = loads(new_cache)
            self.__call_change_callbacks()
        except json.decoder.JSONDecodeError:
            if (self.debug):
                print("Invalid JSON data... Retrying...")
    
    def __compare_and_execute(self):
        while self.__run:
            new_cache = self.__read_string_cache()
                
            if (self.string_cache != new_cache):
                self.string_cache = new_cache
                self.__set_object_cache(new_cache)
                        
            time.sleep(self.refresh_time)
    
    def __call_change_callbacks(self):
        for callback in self.__on_change_callbacks:
            callback()
    
    def get_objects(self):
        return self.__object_cache
    
    def on_change(self, callback: callable):
        self.__on_change_callbacks.append(callback)
    
    def start(self):
        """Starts running the object_stream thread
        """
        self.__run = True
        self.__watch_thread.start()
    
    def stop(self):
        """Stops the object_stream thread
        """
        self.__run = False


def __object_to_dict(object):
    """
    Converts the object to a dictionary, makes it saveable to a JSON.
    Aslo converts every attribute of the object which were objects\n
    `Returns` a dict
    """
    accepted_datatypes: list = [int, str, chr, float, complex, bool, dict, tuple, list]
    new_dict: dict = {}

    if (type(object) is dict):
        new_dict: dict = copy.deepcopy(object)

    if (type(object) is not dict):
        if not hasattr(object, "pyon_converted"):
            new_dict: dict = copy.deepcopy(object).__dict__
        else:
            new_dict = copy.deepcopy(object)._asdict()

        new_dict['PYON_TYPE'] = str(object.__class__.__name__)


    for key, value in new_dict.items():
        if type(value) in [list, tuple]:
            for i, item in enumerate(value):
                if not (type(item) in accepted_datatypes):
                    value[i] = __object_to_dict(item)
        
        if type(value) is dict or hasattr(value, "pyon_converted"):
            for key, value2 in value.items():
                value[key] = __object_to_dict(value2)

        if not (type(value) in accepted_datatypes):
            value = __object_to_dict(value)

    return new_dict


def __dict_to_object(olddict):
    """
    Converts the saved dictionary back to the original object
    #### WARNING: IT WILL NOT CONVERT ANY DICTIONARIES WHICH HAVE NOT BEEN SAVED WITH: "__object_to_dict"\n
    `Returns` the original object
    """
    class_type: str = ""
    params: dict = {}


    if olddict.get('PYON_TYPE'):
        class_type = olddict["PYON_TYPE"];
        olddict.pop("PYON_TYPE", None)
    else:
        class_type = "&DICT"


    for key, value in olddict.items():
        if type(value) is dict:
            value = __dict_to_object(value)

        if type(value) in [list, tuple]:
            for i, item in enumerate(value):
                if type(item) is dict:
                    value[i] = __dict_to_object(item)

        if class_type != "&DICT":
            params[key] = value
        else:
            olddict[key] = value
        
    
    if class_type != "&DICT":
        params["pyon_converted"] = True
        new_object_initializer = namedtuple(class_type, list(params.keys()))
        new_object = new_object_initializer(*list(params.values()))
        
        return new_object

    else:
        return olddict
    

def load_json(_json: str) -> dict: 
    """Loades the data from the _json file

    Args:
        _json (str): load file path

    Returns:
        dict: the json object loaded from the file
    """
    with open(_json, 'r', encoding="utf-8") as read_file:
        loaddata = json.load(read_file)
        return loaddata

def dump_json(_json: str, data: str):
    """Saves the JSON data to _json

    Args:
        _json (str): dist json file path
        data (str): the json object waiting to be saved
    """
    with open(_json, "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)
        write_file.write("\n")

def dump(data: dict or list or object, file: str, indent: int = 4):
    """Works the same as the json.dumps function, but exepts objects as data

    Args:
        data (dict or list or object): object or list or object, will be converted to a dict, and into a JSON
        file (str): filepath
        indent (int, optional): the indentation used in the JSON file. Defaults to 4.
    """
    new_data: dict = __object_to_dict(data) 
    with open(file, "w", encoding="utf-8") as write_file:
        json.dump(new_data, write_file, indent=indent, ensure_ascii=False)
        write_file.write("\n")

def load(file: str) -> object or dict or list:
    """Loads the json file, and converts all the dictionaries which were objects

    Args:
        file (str): filepath 

    Returns:
        object or dict or list: the decoded json
    """
    with open(file, 'r', encoding="utf-8") as read_file:
        loaddata = json.load(read_file)
        return __dict_to_object(loaddata)

def dumps(data: object or dict or list) -> str:
    """Convert an object into a JSON saveable dict.
    #### THIS ALSO CONVERTS EVERY SUB-OBJECT

    Returns:
        str: the encoded object as a string
    """
    return json.dumps(__object_to_dict(data))

def loads(data: str) -> object or dict or list:
    """Convert the saved JSON string back into objects.

    Args:
        data (str): JSON data

    Returns:
        object or dict or list: decoded JSON object
    """
    return __dict_to_object(json.loads(data))
