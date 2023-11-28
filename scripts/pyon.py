from collections import namedtuple
from dataclasses import dataclass
import json
import copy
import threading
import time


"""
PYON VERSION 0.2.0
"""


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
        self.__run = True
        self.__watch_thread.start()
    
    def stop(self):
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
    """
    Loades the data from the _json file
    """
    with open(_json, 'r', encoding="utf-8") as read_file:
        loaddata = json.load(read_file)
        return loaddata

def dump_json(_json: str, data: str):
    """
    Saves the _json file with new data
    """
    with open(_json, "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)
        write_file.write("\n")

def dump(data, file: str, indent: int = 4):
    """
    Works the same as the json.dumps function, but exepts objects as data
    """
    new_data: dict = __object_to_dict(data) 
    with open(file, "w", encoding="utf-8") as write_file:
        json.dump(new_data, write_file, indent=indent, ensure_ascii=False)
        write_file.write("\n")
    pass

def load(file: str):
    """
    Loads the json file, and converts all the dictionaries which were objects
    """
    with open(file, 'r', encoding="utf-8") as read_file:
        loaddata = json.load(read_file)
        return __dict_to_object(loaddata)

def dumps(data):
    """
    Convert an object into a JSON saveable dict.
    #### THIS ALSO CONVERTS EVERY SUB-OBJECT
    """
    return __object_to_dict(data)

def loads(data):
    """
    Convert the saved JSON string back into objects.
    """
    return __dict_to_object(json.loads(data))