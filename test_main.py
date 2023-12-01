
import zenyx
from dataclasses import dataclass
@dataclass
class test:
    testParam: str


def main():
    x = test([[[test("asd")]]])
    print(zenyx.pyon.deep_serialize(x))
    print("Test 1 run successfully")
    
    
if __name__ == "__main__":
    main()