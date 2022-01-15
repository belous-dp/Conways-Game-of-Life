from Cell import Cell
from Position import Position


class BoardInterface:
    default_size = 100
    height: int = default_size
    width: int = default_size

    def get_cell(self, position: Position) -> Cell:
        pass

    def set_cell(self, position: Position, cell: Cell):
        pass

    def set_cell_value(self, position: Position, value: bool):
        pass

    def get_alive_cells_position(self) -> set:
        pass

    def get_sum_of_neighbours(self, position: Position) -> int:
        pass

    def get_neighbours(self, position: Position) -> list:
        pass

    def to_ndarray(self):
        pass

    def invert_cell(self, position: Position):
        pass
