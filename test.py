
import pyon
from dataclasses import dataclass

@dataclass
class test:
    asd: str


def main():
    x = test("asasd")
    y = pyon.object_stream("asds.json")
    
    pyon.dump(x, "asds.json", 4)
    # print(pyon.load("asds.json"))
    
    
if __name__ == "__main__":
    main()

