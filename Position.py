from dataclasses import dataclass


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def __hash__(self):
        return self.x * 10000000 + self.y
