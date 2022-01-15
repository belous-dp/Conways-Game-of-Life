import random

import numpy as np

from BoardInterface import BoardInterface
from Cell import Cell
from Position import Position


class FiniteRectangleBoard(BoardInterface):
    default_size = 100
    height = default_size
    width = default_size
    __NUM_DIRS = 8
    __dx = [-1, -1, -1, 0, 1, 1, 1, 0]
    __dy = [-1, 0, 1, 1, 1, 0, -1, -1]

    def __init__(self, height: int = default_size, width: int = default_size):
        self.height = height
        self.width = width
        self.__board = np.empty([self.height, self.width], dtype=Cell)
        self.__alive = set()
        for i in range(self.height):
            for j in range(self.width):
                self.__board[i][j] = Cell(bool(random.randint(0, 1)))
                if self.__board[i][j].val:
                    self.__alive.add(Position(i, j))
        for i in range(self.height):
            for j in range(self.width):
                self.__board[i][j].sum = self.get_sum_of_neighbours(Position(i, j))
        # print(self.__board.shape)
        # print(self.__board)
        # print(np.zeros([self.__h, self.__w], dtype=bool))

    def in_field(self, position: Position):
        return 0 <= position.x < self.height and 0 <= position.y < self.width

    def get_cell(self, position: Position):
        return self.__board[position.x][position.y]

    def set_cell(self, position: Position, cell: Cell):
        self.__board[position.x][position.y] = cell

    def set_cell_value(self, position: Position, value: bool):
        self.__board[position.x][position.y].val = value
        if self.__board[position.x][position.y].is_alive():
            self.__alive.add(position)
        else:
            self.__alive.remove(position)

    def get_alive_cells_position(self) -> set:
        return self.__alive

    def get_sum_of_neighbours(self, position: Position) -> int:
        res = 0
        for i in range(self.__NUM_DIRS):
            neighbour = Position(position.x + self.__dx[i], position.y + self.__dy[i])
            if self.in_field(neighbour) and self.__board[neighbour.x][neighbour.y].is_alive():
                res += 1
        return res

    def get_neighbours(self, position: Position) -> list:
        res = []
        for i in range(self.__NUM_DIRS):
            neighbour = Position(position.x + self.__dx[i], position.y + self.__dy[i])
            if self.in_field(neighbour):
                res.append(neighbour)
        return res

    def to_ndarray(self):
        res = np.empty([self.height, self.width], dtype=bool)
        for i in range(self.height):
            for j in range(self.width):
                res[i][j] = self.__board[i][j].val
        return res

    def invert_cell(self, position: Position):
        self.__board[position.x][position.y].invert()


