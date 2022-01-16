from Cell import Cell
from Position import Position


class BoardInterface:
    def get_cell(self, pos: Position) -> Cell:
        pass

    def set_cell(self, pos: Position, cell: Cell):
        pass

    def get_cell_neighbours(self, pos: Position) -> list[Position]:
        pass

    def make_move(self):
        pass

    def add_glider(self, pos: Position):
        pass

    def to_2d_array(self):
        pass
