
import zenyx
from dataclasses import dataclass
@dataclass
class test:
    testParam: str


def main():
    zenyx.pyon.debug()
    
    x = test([[[test("asd")]]])
    y = zenyx.pyon.deep_serialize(x)
    print(zenyx.pyon.deep_parse(y))
    print("Test 1 run successfully")
    
    
if __name__ == "__main__":
    main()