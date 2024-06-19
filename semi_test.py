from dataclasses import dataclass
import src.zenyx as zenyx
import math

@zenyx.struct
class Vec2:
    x: int = 0
    y: int = 0

    def add(self: "Vec2") -> int:
        return self.x + self.y
