
import nyxerium
from dataclasses import dataclass
import timeit

@dataclass
class test:
    testParam: str


def main():
    
    nyxerium.pyon.debug()
    
    x = test({"dictKey": [{"listElement0": test("listElement1DictObject")}, test("listElement2Param")]})
    
    def testf():
        nyxerium.pyon.deep_serialize(x)
        return
    
    time_elapsed = timeit.timeit(testf, number=1)
    print(time_elapsed)
    
    nyxerium.pyon.dump(x, "test.json")
    
    
if __name__ == "__main__":
    main()

