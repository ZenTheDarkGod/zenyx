
import zenyx
from dataclasses import dataclass
@dataclass
class test:
    testParam: str


def main():
    x = test("asd")
    assert zenyx.pyon.dumps(x) == '{"testParam": "asd", "PYON_TYPE": "test"}'
    
    
