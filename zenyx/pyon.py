
import datetime
import json
import copy
from collections import namedtuple

__debug_setting: bool = False

def __get_console_time():
    # Get the current time
    current_time = datetime.datetime.now().time()
    # Format the time as "hh:mm:ss:ms"
    formatted_time = current_time.strftime("%H:%M:%S:%f")[:-3]
    return formatted_time

def debug():
    """
    ## THIS WILL SLOW DOWN PYON BY ~300%
    Enables the debug feature.
    The debug file will be saved as `pyon.debug.txt`.\n
    For now it only contains the following:
    - deep_serialize
    - deep_parse
    """
    global __debug_setting
    __debug_setting = True
    with open("pyon.debug.txt", "w") as write:
        write.write("")


def __debug(*args: list):
    global __debug_setting
    if (__debug_setting):
        print(*args)
        time_text = f"\n{__get_console_time()} | "
        with open("pyon.debug.txt", "a") as wf:
            wf.write(time_text)
            for arg in args:
                if type(arg) is str:
                    wf.write(arg.replace("\n", time_text))
                else:
                    wf.write(str(arg).replace("\n", time_text))
                wf.write(" ")


def is_type(value: any, _type):
    __debug(f"  [TypeCheck] Value: {value}, Type(s): {_type}")
    if type(value) is _type:
        return True
    if type(_type) in [list, tuple]:
        if type(value) in _type:
            return True
    return False


__indent = 1


def deep_serialize(obj: any) -> dict:
    __debug(f"\n[Deep Serialize] Object: {obj}")
    global __debug_setting
    xdent = 1
    if __debug_setting:
        global __indent
        xdent = copy.deepcopy(__indent)
        __indent += 1
        
    __debug(f"\n[Start - {xdent}]","="*20)
    
    """Converts the object to a dictionary, makes it saveable to a JSON.
    Aslo converts every attribute of the object which were objects\n
    Args:
        obj (any): the object you wish wo deep convert
    Returns:
        dict: _description_
    """
    
    __debug(f"  [{xdent}] Original obj input:\n", f"\t{obj}")
    
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
        if (is_type(value, (dict, list, tuple))):
            test1 = True
        
        __debug(f"  [{xdent}] Value for Iterability test:\n", 
                   f"\tvalue: {value} @type: {type(value)} | is the value an object (__is_object): {__is_object(value)} | is the value a dict/list/tuple (test1): {test1}\n"
                   f"\tFinal Resoult: {__is_object(value) or test1}")
        
        return __is_object(value) or test1
    
    # If the obj is not iterable, return
    __debug(f"  [{xdent}] Original Obj Iterability (Good if False):\n", f"\tObject (obj): {obj} | is object iterable: {__is_iterable(obj)}")
    if not __is_iterable(obj):
        __debug(f"[Early End - {xdent}] Not Iterable","="*20,"\n")
        return obj
    # If the obj is already a dict, just use it as the base
    if (is_type(obj, dict)):
        new_dict: dict = copy.deepcopy(obj)
        
    # DO NOT FUCK WITH THIS FOR CHIRST'S SAKE MAN IT WILL BREAK
    # SWEAR TO GOD I DON'T KNOW HOW THIS WORKS AND I DON'T EVEN WANT TO
    # PLEASE DO NOT TOUCH IT
    #                                   - zewenn 30/11/2023
    # =====================================================================
    # So this checks if the obj is not a dict, and it also checks if the obj is an object (`hasattr(obj, "__dict__")`) or a namedtuple (`hasattr(obj, "_asdict"))`)
    #                                   - zewenn 01/12/2023
    if (not is_type(obj, dict)) and (hasattr(obj, "__dict__") or hasattr(obj, "_asdict")):
        # if it's not a pyon converted named tuple -> it's an object
        if not hasattr(obj, "pyon_converted") or not hasattr(obj, "_asdict"):
            new_dict: dict = copy.deepcopy(obj).__dict__
        else:
            # it's a namedtuple
            new_dict = copy.deepcopy(obj)._asdict()
        new_dict['PYON_TYPE'] = str(obj.__class__.__name__)
        
    # Handling list[list[list[object]]] edge cases
    if (is_type(obj, (list, tuple))):
        for index, element in enumerate(obj):
            __debug(f"  [{xdent}] Iterating list/tuple:\n", f"\t List/Tuple (obj): {obj} | Element: {element}")
            if __is_iterable(element):
                obj[index] = deep_serialize(element)
        
        __debug(f"[Early End - {xdent}] List Serialized","="*20,"\n")
        return obj
    for key, value in new_dict.items():
        # Object(ls=[Object2()])
        if is_type(value, (list, tuple)): 
            for i, item in enumerate(value):
                if __is_iterable(item):
                    value[i] = deep_serialize(item)
        
        # Object(asd={asd: Object2()})
        if is_type(value, dict) or hasattr(value, "pyon_converted"):
            for key, value2 in value.items():
                if __is_iterable(value2):
                    value[key] = deep_serialize(value2)
        # value is Object
        if __is_object(value):
            new_dict[key] = deep_serialize(value)
    __debug(f"  [{xdent}] New dict created:\n", f"\t{new_dict}")
    __debug(f"[End - {xdent}]","="*20,"\n")
    return new_dict

def deep_parse(olddict: dict or list) -> object or dict:
    """
    #### WARNING: IT WILL NOT CONVERT ANY DICTIONARIES WHICH HAVE NOT BEEN SAVED WITH: "__object_to_dict"\n
    Converts the saved dictionary back to the original object
    `Returns` the original object
    """
    class_type: str = ""
    params: dict = {}
    
    
    xdent = 1
    if __debug_setting:
        global __indent 
        xdent = copy.deepcopy(__indent)
        __indent += 1
        
    __debug(f"\n[Deep Parse] Dict/List: {olddict}")
    __debug(f"\n[Start - {xdent}]","="*20)
    if is_type(olddict, list):
        olddict = {"&ORIGINAL_LIST" : olddict}
    if olddict.get('PYON_TYPE'):
        class_type = olddict["PYON_TYPE"]
        olddict.pop("PYON_TYPE", None)
    else:
        class_type = "&DICT"
    # not using is_type() bc of performance
    for key, value in olddict.items():
        if type(value) is dict:
            value = deep_parse(value)
        if type(value) in [list, tuple]:
            for i, item in enumerate(value):
                if type(item) is dict:
                    value[i] = deep_parse(item)
        if class_type != "&DICT":
            params[key] = value
            continue
        olddict[key] = value
        
    if olddict.get("&ORIGINAL_LIST"):
        olddict = olddict.get("&ORIGINAL_LIST")
        __debug(f"  [{xdent}] Restored Original List:\n  \t{olddict}")
        
    def __end(text: any):
        __debug(f"  [{xdent}] Return Value: {text}")
        __debug(f"[End - {xdent}]","="*20,"\n")
    
    if class_type != "&DICT":
        params["pyon_converted"] = True
        new_object_initializer = namedtuple(class_type, list(params.keys()))
        new_object = new_object_initializer(*list(params.values()))
        
        __end(new_object)
        return new_object
    __end(olddict)
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
    new_data: dict = deep_serialize(data) 
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
        return deep_parse(loaddata)

def dumps(data: object or dict or list) -> str:
    """Convert an object into a JSON saveable dict.
    #### THIS ALSO CONVERTS EVERY SUB-OBJECT
    Returns:
        str: the encoded object as a string
    """
    return json.dumps(deep_serialize(data))

def loads(data: str) -> object or dict or list:
    """Convert the saved JSON string back into objects.
    Args:
        data (str): JSON data
    Returns:
        object or dict or list: decoded JSON object
    """
    return deep_parse(json.loads(data))