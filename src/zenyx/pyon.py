
import datetime
import json
import copy
from collections import namedtuple
from dataclasses import dataclass
import re
import os

__debug_setting: bool = False
__debug_file: str = "pyon.debug.md"
__debug_path: str = ""

# Done
# def __get_console_time():
#     # Get the current time
#     current_time = datetime.datetime.now().time()
#     # Format the time as "hh:mm:ss:ms"
#     formatted_time = current_time.strftime("%H:%M:%S:%f")[:-3]
#     return formatted_time

# Done
# def debug(path: str):
#     """## THIS WILL SLOW DOWN PYON BY ~300%
#     Enables the debug feature.
#     The debug file will be saved as `pyon.debug.txt`.\n
#     For now it only contains the following:
#     - deep_serialize
#     - deep_parse

#     Args:
#         path (str): just use `__file__`
#     """
#     global __debug_setting
#     global __debug_file
#     global __debug_path
    
#     __debug_path = os.path.join(os.path.dirname(os.path.abspath(path)), __debug_file)
    
#     __debug_setting = True
#     with open(__debug_path, "w") as write:
#         write.write("")

# done
# def __debug(*args: str):
#     global __debug_setting
#     global __debug_file
    
#     if (__debug_setting):
#         print(*args)
#         time_text = f"\n<br>`{__get_console_time()}` | "
        
#         def replace_newlines(input_string, _with):
#             # Define a pattern to match newline characters outside triple backticks
#             pattern = re.compile(r'(```[^`]*```)|\n')

#             # Replace newline characters with the specified replacement except those inside triple backticks
#             result_string = pattern.sub(lambda match: match.group(1) if match.group(1) else _with, input_string)

#             return result_string
        
#         with open(__debug_path, "a") as wf:
#             wf.write(time_text)
#             __arglist = list(args)
#             __arglist.append("\n")
#             for arg in __arglist:
#                 if (arg.startswith("\t")):
#                     arglist = list(arg)
#                     arglist.insert(0, "  ")
#                     arg = "Đ".join(arglist).replace("Đ", "")
#                 if (arg.__contains__("\n\t")):
#                     arg = arg.replace("\n\t", "\n  \t")
                    
#                 arg = arg.replace("\t", "\t&emsp;")
#                 arg = replace_newlines(arg, time_text)
#                 # arg = replace_newlines(arg, "<br>")
                
                    
#                 wf.write(arg)

# def __debug_separator(*args, xdent: int = 1, callbackorigin: int = 0, text: str = "", title: str = ""):
#     callbackorigin_text = ""
#     xdent_text = ""
#     length = 64
    
#     if (callbackorigin != 0):
#         callbackorigin_text = f" - Caller: {callbackorigin}"
    
#     if (xdent != 0):
#         xdent_text = f": {xdent}"
        
#     if (text != ""):
#         text = f" {text}"
        
#     line_start_text = f" [{title}{xdent_text}{callbackorigin_text}]{text} "
#     spacing = "="*(int((length-len(line_start_text))/2))
#     ret_text = f"{spacing}{line_start_text}{spacing}"
    
#     return (f"\n**`{ret_text[0:length]}`**\n")

def is_type(value: any, _type):
    debugf.log(f"  **`[TypeCheck]`** Checking Type \n\tValue: `{value}`, \n\tType(s): `{_type}`")
    if type(value) is _type:
        return True
    if type(_type) in [list, tuple]:
        if type(value) in _type:
            return True
    return False







class debugf:
    class debug_object:
        def __init__(self, path, *args: str, debug_file: str = "") -> None:
            self.path: str
            self.debug_file: str = "pyon.debug.md"
            if debug_file != "":
                self.debug_file = debug_file
            
            self.__debug_path = os.path.join(os.path.dirname(os.path.abspath(self.path)), self.debug_file)
            
            
    
    debugger: debug_object or None
    __indent = 1
    
    @staticmethod
    def create(path, *args: str, filename: str = ""):
        """## THIS WILL SLOW DOWN PYON BY ~300%
        Enables the debug feature.
        The debug file will be saved as `pyon.debug.txt`.\n
        For now it only contains the following:
        - deep_serialize
        - deep_parse

        Args:
            path (str): just use `__file__`
        """
        if debugf.debugger != None:
                debugf.debugger = debugf.debug_object(path=path, debug_file=filename)
        else:
            raise Exception("Can't initalize multiple debuggers :(")
    
    @staticmethod
    def __get_console_time():
        # Get the current time
        current_time = datetime.datetime.now().time()
        # Format the time as "hh:mm:ss:ms"
        formatted_time = current_time.strftime("%H:%M:%S:%f")[:-3]
        return formatted_time
    
    @staticmethod
    def log(*args: str):
        if debugf.debugger == None:
            return
        
        print(*args)
        time_text = f"\n<br>`{debugf.__get_console_time()}` | "
        
        def replace_newlines(input_string, _with):
            # Define a pattern to match newline characters outside triple backticks
            pattern = re.compile(r'(```[^`]*```)|\n')

            # Replace newline characters with the specified replacement except those inside triple backticks
            result_string = pattern.sub(lambda match: match.group(1) if match.group(1) else _with, input_string)

            return result_string
        
        with open(debugf.debugger.__debug_path, "a") as wf:
            wf.write(time_text)
            __arglist = list(args)
            __arglist.append("\n")
            for arg in __arglist:
                if (arg.startswith("\t")):
                    arglist = list(arg)
                    arglist.insert(0, "  ")
                    arg = "Đ".join(arglist).replace("Đ", "")
                if (arg.__contains__("\n\t")):
                    arg = arg.replace("\n\t", "\n  \t")
                    
                arg = arg.replace("\t", "\t&emsp;")
                arg = replace_newlines(arg, time_text)
                
                    
                wf.write(arg)
    
    @staticmethod
    def separator_text(*args, xdent: int = 1, callbackorigin: int = 0, text: str = "", title: str = ""):
        callbackorigin_text = ""
        xdent_text = ""
        length = 64
        
        if (callbackorigin != 0):
            callbackorigin_text = f" - Caller: {callbackorigin}"
        
        if (xdent != 0):
            xdent_text = f": {xdent}"
            
        if (text != ""):
            text = f" {text}"
            
        line_start_text = f" [{title}{xdent_text}{callbackorigin_text}]{text} "
        spacing = "="*(int((length-len(line_start_text))/2))
        ret_text = f"{spacing}{line_start_text}{spacing}"
        
        return (f"\n**`{ret_text[0:length]}`**\n")

def deep_serialize(obj: any, *args, callbacktime:int = 0) -> dict:
    debugf.log(debugf.separator_text(title="Deep Serialize", xdent=0, callbackorigin=callbacktime))
    global __debug_setting
    xdent = 1
    if __debug_setting:
        xdent = copy.deepcopy(debugf.__indent)
        debugf.__indent += 1
        
    # __debug(f"\n[Start - {xdent} - Caller: {callbacktime}]","="*20)
    debugf.log(debugf.separator_text(title="Start", xdent=xdent, callbackorigin=callbacktime))
    
    """Converts the object to a dictionary, makes it saveable to a JSON.
    Aslo converts every attribute of the object which were objects\n
    Args:
        obj (any): the object you wish wo deep convert
    Returns:
        dict: _description_
    """
    
    debugf.log(f"  **`[{xdent}]`** Original obj input:\n", f"\t`{obj}`")
    
    new_dict: dict = {}

    # If somehow it isn't an object, just return the value
    # (this is a miracle since almost everything is an object :"D)
    if not isinstance(obj, object):
        return obj
    
    def __self_call(obj: any):
        return deep_serialize(obj, callbacktime=xdent)
    
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
        
        debugf.log(f"  **`[{xdent}]`** Iterability test:\n", 
                   f"\t**Params:**\n\t\tValue: `{value}`\n\t\t@Type: `{type(value)}`\n",
                   f"\tIs object *(`__is_object`)*: `{__is_object(value)}`\n",
                   f"\tIs dict/list/tuple *(`test1`)*: `{test1}`\n",
                   f"\t**Final Resoult**: `{__is_object(value) or test1}`")
        
        return __is_object(value) or test1
    
    # If the obj is not iterable, return
    debugf.log(f"  **`[{xdent}]`** Original Obj Iterability *(can be `False`)*:\n", f"\tObject *(`obj`)*: `{obj}` \n\t**Is object iterable**: `{__is_iterable(obj)}`")
    if not __is_iterable(obj):
        debugf.log(debugf.separator_text(title="Early End", text="Not Iterable", xdent=xdent, callbackorigin=callbacktime))
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
            debugf.log(f"  **`[{xdent}]`** Iterating List/Tuple:\n", f"\tList/Tuple *(`obj`)*: `{obj}`\n\tElement: `{element}`")
            if __is_iterable(element):
                obj[index] = __self_call(element)
        
        debugf.log(debugf.separator_text(title="Early End", text="List Serialized", xdent=xdent, callbackorigin=callbacktime))
        return obj
    
    # At this point new_dict is a dictionary, containing all keys and all values of the object/dict
    for key, value in new_dict.items():
        # Object(ls=[Object2()])
        if is_type(value, (list, tuple)): 
            for i, item in enumerate(value):
                if __is_iterable(item):
                    value[i] = __self_call(item)
        
        # Object(asd={asd: Object2()})
        if is_type(value, dict) or hasattr(value, "pyon_converted"):
            for key, value2 in value.items():
                if __is_iterable(value2):
                    value[key] = __self_call(value2)
        # value is Object
        if __is_object(value):
            new_dict[key] = __self_call(value)
    
    debugf.log(f"  **`[{xdent}]`** **New dict created:**\n", f"\t`{new_dict}`")
    debugf.log(debugf.separator_text(title="End", xdent=xdent, callbackorigin=callbacktime))
    
    if (xdent == 1):
        debugf.__indent = 1
    
    return new_dict



def deep_parse(olddict: dict or list, *args: str, callbacktime: int = 0) -> object or dict:
    """
    #### WARNING: IT WILL NOT CONVERT ANY DICTIONARIES WHICH HAVE NOT BEEN SAVED WITH: "__object_to_dict"\n
    Converts the saved dictionary back to the original object
    `Returns` the original object
    """
    class_type: str = ""
    params: dict = {}
    
    debugf.log(debugf.separator_text(title="Deep Parse", xdent=0, callbackorigin=callbacktime))
    
    xdent = 1
    if __debug_setting:
        xdent = copy.deepcopy(debugf.__indent)
        debugf.__indent += 1
        
    
    def __self_call(obj: any):
        return deep_parse(obj, callbacktime=xdent)
        
    # __debug(f"\n[Deep Parse] Dict/List: {olddict}")
    debugf.log(debugf.separator_text(title="Start", xdent=xdent, callbackorigin=callbacktime))
    
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
            value = __self_call(value)
            
        if type(value) in [list, tuple]:
            for i, item in enumerate(value):
                if type(item) in [dict, list, tuple]:
                    value[i] = __self_call(item)
                    
        if class_type != "&DICT":
            params[key] = value
            continue
        olddict[key] = value
        
    if olddict.get("&ORIGINAL_LIST"):
        olddict = olddict.get("&ORIGINAL_LIST")
        debugf.log(f"  **`[{xdent}]`** Restored Original List:\n  \t`{olddict}`")
        
    def __end(text: any):
        debugf.log(f"  **`[{xdent}]`** Return Value: \n\t`{text}`")
        debugf.log(debugf.separator_text(title="End", xdent=xdent, callbackorigin=callbacktime))
    
    if class_type != "&DICT":
        params["pyon_converted"] = True
        new_object_initializer = namedtuple(class_type, list(params.keys()))
        new_object = new_object_initializer(*list(params.values()))
        
        __end(new_object)
        return new_object
    __end(olddict)
    
    
    if (xdent == 1):
        debugf.__indent = 1
    
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