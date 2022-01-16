from dataclasses import dataclass  # чтобы не писать __init__


@dataclass
class Position:
    x: int = 0
    y: int = 0

    def __hash__(self):
        return (self.x * 0x1f1f1f1f) ^ self.y  # какой-то достаточно сильный хэш
