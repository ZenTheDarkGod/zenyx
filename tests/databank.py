from dataclasses import dataclass


@dataclass
class test:
    param: any

demo_obj = test([test({"test": 0}), "asd"])