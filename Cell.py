from dataclasses import dataclass  # чтобы не писать __init__


@dataclass
class Cell:
    val: bool = False
    sum: int = 0

    # В принципе мало какие из этих методов нужны, но раз уж создавать отдельный класс для bool'а, то давайте как-нибудь
    # пафосно назовём их
    def is_alive(self):
        return self.val

    def is_dead(self):
        return not self.is_alive()

    def invert(self):
        self.val = not self.val
