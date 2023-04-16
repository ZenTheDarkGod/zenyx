from collections import namedtuple
import json
import copy


# Converts the object to a dictionary
# Aslo converts every attribute of the object which were objects
# Makes the object saveable to a JSON
def __object_to_dict(object):
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


# Converts the saved dictionary back to the original object
# WARNING: IT WILL NOT CONVERT ANY DICTIONARIES WHICH HAVE NOT BEEN SAVED WITH: "__object_to_dict"
# Returns the original object
def __dict_to_object(olddict):
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
    


# Loades the data from the _json file
def load_json(_json: str) -> dict: 
    with open(_json, 'r', encoding="utf-8") as read_file:
        loaddata = json.load(read_file)
        return loaddata

# Saves the _json file with new data
def dump_json(_json: str, data: str):
    with open(_json, "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)
        write_file.write("\n")

# Works the same as the json.dumps function, but exepts objects as data
def dump(data, file: str, indent: int = 4):
    new_data: dict = __object_to_dict(data) 
    with open(file, "w", encoding="utf-8") as write_file:
        json.dump(new_data, write_file, indent=indent, ensure_ascii=False)
        write_file.write("\n")
    pass

# Loads the json file, and converts all the dictionaries which were objects
def load(file: str):
    with open(file, 'r', encoding="utf-8") as read_file:
        loaddata = json.load(read_file)
        return __dict_to_object(loaddata)

def dumps(data):
    return __object_to_dict(data)

def loads(data):
    return __dict_to_object(json.loads(data))