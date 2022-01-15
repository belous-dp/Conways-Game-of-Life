from dataclasses import dataclass


@dataclass
class Cell:
    val: bool = False
    sum: int = 0

    def is_alive(self):
        return self.val

    def is_dead(self):
        return not self.is_alive()

    def invert(self):
        self.val = not self.val
