"""
# nyxerium
version 0.3.1\n

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

from collections import namedtuple
import json
import copy
import threading
import time, datetime
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
            self.__object_cache = pyon.loads(new_cache)
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

class pyon:
    
    __debug_setting: bool = False
    __debug_log: str = ""
    
    def __get_console_time():
        # Get the current time
        current_time = datetime.datetime.now().time()

        # Format the time as "hh:mm:ss:ms"
        formatted_time = current_time.strftime("%H:%M:%S:%f")[:-3]

        return formatted_time
    
    @staticmethod
    def debug():
        """
        ## THIS WILL SLOW DOWN PYON BY ~300%
        Enables the debug feature.
        The debug file will be saved as `nyxerium.pyon.debug.txt`.\n
        For now it only contains the following:
        - deep_serialize
        - deep_parse
        """
        pyon.__debug_setting = True
        with open("nyxerium.pyon.debug.txt", "w") as write:
            write.write("")
    
    @staticmethod
    def __debug(*args: list):
        if (pyon.__debug_setting):
            print(*args)
            time_text = f"\n{pyon.__get_console_time()} | "
            with open("nyxerium.pyon.debug.txt", "a") as wf:
                wf.write(time_text)
                for arg in args:
                    if type(arg) is str:
                        wf.write(arg.replace("\n", time_text))
                    else:
                        wf.write(str(arg).replace("\n", time_text))
                    wf.write(" ")
    
    @staticmethod
    def is_type(value: any, _type):
        pyon.__debug(f"  [TypeCheck] Value: {value}, Type(s): {_type}")
        if type(value) is _type:
            return True
        if type(_type) in [list, tuple]:
            if type(value) in _type:
                return True
        return False
    
    
    __indent = 1
    
    @staticmethod
    def deep_serialize(obj: any) -> dict:
        pyon.__debug(f"\n[Deep Serialize] Object: {obj}")
        
        xdent = 1
        if pyon.__debug_setting:
            xdent = copy.deepcopy(pyon.__indent)
            pyon.__indent += 1
            
        pyon.__debug(f"\n[Start - {xdent}]","="*20)
        
        """Converts the object to a dictionary, makes it saveable to a JSON.
        Aslo converts every attribute of the object which were objects\n

        Args:
            obj (any): the object you wish wo deep convert

        Returns:
            dict: _description_
        """
        
        pyon.__debug(f"  [{xdent}] Original obj input:\n", f"\t{obj}")
        
        new_dict: dict = {}
    
        # If somehow it isn't an object, just return the value
        # (this is a miracle since almost everything is an object :"D)
        if not isinstance(obj, object):
            return obj
        
        def __is_object(value: any) -> bool:
            """Check if the value is an object by comparing it to all other default python datatypes

            Args:
                value (any): the value you wish to compare

            Returns:
                bool: whether the value is an object or not
            """
            excluded_types = (int, float, complex, str, bool, list, tuple, dict, set)
            return (hasattr(value, "__dict__") and not isinstance(value, excluded_types))
        
        def __is_iterable(value: any) -> bool:
            """### THIS IS AN INNER FUNCTION, CAN'T BE USED ELSEWHERE
            checks if you can iterate the value by the parent function's recursion

            Args:
                value (any): the value you wish to check

            Returns:
                bool: whether the value is iterable or not
            """
            # True if fails
            test1: bool = False
            if (pyon.is_type(value, (dict, list, tuple))):
                test1 = True
            
            pyon.__debug(f"  [{xdent}] Value for Iterability test:\n", 
                       f"\tvalue: {value} @type: {type(value)} | is the value an object (__is_object): {__is_object(value)} | is the value a dict/list/tuple (test1): {test1}\n"
                       f"\tFinal Resoult: {__is_object(value) or test1}")
            
            return __is_object(value) or test1
        
        # If the obj is not iterable, return
        pyon.__debug(f"  [{xdent}] Original Obj Iterability (Good if False):\n", f"\tObject (obj): {obj} | is object iterable: {__is_iterable(obj)}")
        if not __is_iterable(obj):
            pyon.__debug(f"[Early End - {xdent}] Not Iterable","="*20,"\n")
            return obj

        # If the obj is already a dict, just use it as the base
        if (pyon.is_type(obj, dict)):
            new_dict: dict = copy.deepcopy(obj)

        # DO NOT FUCK WITH THIS FOR CHIRST'S SAKE MAN IT WILL BREAK
        # SWEAR TO GOD I DON'T KNOW HOW THIS WORKS AND I DON'T EVEN WANT TO
        # PLEASE DO NOT TOUCH IT
        #                                   - zewenn 30/11/2023
        if (not pyon.is_type(obj, dict)) and (hasattr(obj, "__dict__") or hasattr(obj, "_asdict")):
            if not hasattr(obj, "pyon_converted"):
                new_dict: dict = copy.deepcopy(obj).__dict__
            else:
                new_dict = copy.deepcopy(obj)._asdict()

            new_dict['PYON_TYPE'] = str(obj.__class__.__name__)

        # Handling list[list[list[object]]] edge cases
        if (pyon.is_type(obj, (list, tuple))):
            for index, element in enumerate(obj):
                pyon.__debug(f"  [{xdent}] Iterating list/tuple:\n", f"\t List/Tuple (obj): {obj} | Element: {element}")
                if __is_iterable(element):
                    obj[index] = pyon.deep_serialize(element)
            
            pyon.__debug(f"[Early End - {xdent}] List Serialized","="*20,"\n")
            return obj

        for key, value in new_dict.items():
            # Object(ls=[Object2()])
            if pyon.is_type(value, (list, tuple)): 
                for i, item in enumerate(value):
                    if __is_object(item) or pyon.is_type(item, dict):
                        value[i] = pyon.deep_serialize(item)
            
            # Object(asd={asd: Object2()})
            if pyon.is_type(value, dict) or hasattr(value, "pyon_converted"):
                for key, value2 in value.items():
                    if __is_iterable(value2):
                        value[key] = pyon.deep_serialize(value2)

            # value is Object
            if __is_object(value):
                new_dict[key] = pyon.deep_serialize(value)

        pyon.__debug(f"  [{xdent}] New dict created:\n", f"\t{new_dict}")
        pyon.__debug(f"[End - {xdent}]","="*20,"\n")
        return new_dict


    @staticmethod
    def deep_parse(olddict: dict or list) -> object or dict:
        """
        #### WARNING: IT WILL NOT CONVERT ANY DICTIONARIES WHICH HAVE NOT BEEN SAVED WITH: "__object_to_dict"\n
        Converts the saved dictionary back to the original object
        `Returns` the original object
        """
        class_type: str = ""
        params: dict = {}
        
        
        xdent = 1
        if pyon.__debug_setting:
            xdent = copy.deepcopy(pyon.__indent)
            pyon.__indent += 1
            
        pyon.__debug(f"\n[Deep Parse] Dict/List: {olddict}")
        pyon.__debug(f"\n[Start - {xdent}]","="*20)

        if pyon.is_type(olddict, list):
            olddict = {"&ORIGINAL_LIST" : olddict}

        if olddict.get('PYON_TYPE'):
            class_type = olddict["PYON_TYPE"]
            olddict.pop("PYON_TYPE", None)
        else:
            class_type = "&DICT"

        # not using pyon.is_type() bc of performance

        for key, value in olddict.items():
            if type(value) is dict:
                value = pyon.deep_parse(value)

            if type(value) in [list, tuple]:
                for i, item in enumerate(value):
                    if type(item) is dict:
                        value[i] = pyon.deep_parse(item)

            if class_type != "&DICT":
                params[key] = value
                continue
            olddict[key] = value
            
        if olddict.get("&ORIGINAL_LIST"):
            olddict = olddict.get("&ORIGINAL_LIST")
            pyon.__debug(f"  [{xdent}] Restored Original List:\n  \t{olddict}")
            
        def __end(text: any):
            pyon.__debug(f"  [{xdent}] Return Value: {text}")
            pyon.__debug(f"[End - {xdent}]","="*20,"\n")
        
        if class_type != "&DICT":
            params["pyon_converted"] = True
            new_object_initializer = namedtuple(class_type, list(params.keys()))
            new_object = new_object_initializer(*list(params.values()))
            
            __end(new_object)
            return new_object

        __end(olddict)
        return olddict
        

    @staticmethod
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

    @staticmethod
    def dump_json(_json: str, data: str):
        """Saves the JSON data to _json

        Args:
            _json (str): dist json file path
            data (str): the json object waiting to be saved
        """
        with open(_json, "w", encoding="utf-8") as write_file:
            json.dump(data, write_file, indent=4, ensure_ascii=False)
            write_file.write("\n")

    @staticmethod
    def dump(data: dict or list or object, file: str, indent: int = 4):
        """Works the same as the json.dumps function, but exepts objects as data

        Args:
            data (dict or list or object): object or list or object, will be converted to a dict, and into a JSON
            file (str): filepath
            indent (int, optional): the indentation used in the JSON file. Defaults to 4.
        """
        new_data: dict = pyon.deep_serialize(data) 
        with open(file, "w", encoding="utf-8") as write_file:
            json.dump(new_data, write_file, indent=indent, ensure_ascii=False)
            write_file.write("\n")

    @staticmethod
    def load(file: str) -> object or dict or list:
        """Loads the json file, and converts all the dictionaries which were objects

        Args:
            file (str): filepath 

        Returns:
            object or dict or list: the decoded json
        """
        with open(file, 'r', encoding="utf-8") as read_file:
            loaddata = json.load(read_file)
            return pyon.deep_parse(loaddata)

    @staticmethod
    def dumps(data: object or dict or list) -> str:
        """Convert an object into a JSON saveable dict.
        #### THIS ALSO CONVERTS EVERY SUB-OBJECT

        Returns:
            str: the encoded object as a string
        """
        return json.dumps(pyon.deep_serialize(data))

    @staticmethod
    def loads(data: str) -> object or dict or list:
        """Convert the saved JSON string back into objects.

        Args:
            data (str): JSON data

        Returns:
            object or dict or list: decoded JSON object
        """
        return pyon.deep_parse(json.loads(data))


