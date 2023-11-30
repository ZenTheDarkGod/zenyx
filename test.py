
import zenyx
from dataclasses import dataclass
import timeit

@dataclass
class test:
    testParam: str


def main():
    
    zenyx.pyon.debug()
    
    y = test(["testDataaa", test("nem")])
    
    zenyx.pyon.dump(y, "test.json")
    
    x = zenyx.pyon.load("test.json")
    
    print(x)
    
    
    
if __name__ == "__main__":
    main()

