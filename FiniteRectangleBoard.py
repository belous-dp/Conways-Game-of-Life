import numpy as np

import Grid
from BoardInterface import BoardInterface
from Cell import Cell
from Position import Position


class FiniteRectangleBoard(BoardInterface):
    default_size = 100
    __NUM_DIRS = 8
    __dx = [-1, -1, -1, 0, 1, 1, 1, 0]
    __dy = [-1, 0, 1, 1, 1, 0, -1, -1]

    def __init__(self, height: int = default_size, width: int = default_size):
        self.__height = height
        self.__width = width
        self.__board = Grid.random_grid(height, width)
        # self.__board = np.empty([self.height, self.width], dtype=Cell)
        # self.__alive = set()
        # for i in range(self.height):
        #     for j in range(self.width):
        #         self.__board[i][j] = Cell(bool(random.randint(0, 1)))
        #         if self.__board[i][j].val:
        #             self.__alive.add(Position(i, j))
        for i in range(self.__height):
            for j in range(self.__width):
                self.__board[i][j].sum = self.__get_sum_of_neighbouring_cells(Position(i, j))

    def get_cell(self, pos: Position) -> Cell:
        # TODO: обработку ошибок выхода за границы
        return self.__board[pos.x][pos.y]

    def set_cell(self, pos: Position, cell: Cell):
        # TODO: обработку ошибок выхода за границы
        self.__board[pos.x][pos.y] = cell

    def get_cell_neighbours(self, pos: Position) -> list[Position]:
        res = []
        for i in range(self.__NUM_DIRS):
            neighbour = Position(pos.x + self.__dx[i], pos.y + self.__dy[i])
            if self.__is_in_board(neighbour):
                res.append(neighbour)
        return res

    def __is_in_board(self, pos: Position):
        return 0 <= pos.x < self.__height and 0 <= pos.y < self.__width

    def __set_cell_value(self, pos: Position, value: bool):
        self.__board[pos.x][pos.y].val = value
        # if self.__board[pos.x][pos.y].is_alive():
        #     self.__alive.add(pos)
        # else:
        #     self.__alive.remove(pos)

    # def get_alive_cells_position(self) -> set[Position]:
    #     return self.__alive

    def __get_sum_of_neighbouring_cells(self, pos: Position) -> int:
        res = 0
        for neighbour_pos in self.get_cell_neighbours(pos):
            if self.__board[neighbour_pos.x][neighbour_pos.y].is_alive():
                res += 1
        return res

    def make_move(self):
        # next_alive = set()
        changed = set()
        # for pos in self.__interesting:
        #     cell = self.__board.get_cell(pos)
        #     sum = self.__board.get_sum_of_neighbours(pos)
        #     if cell.is_alive() and (sum == 2 or sum == 3):
        #         next_alive.add(pos)
        #     elif cell.is_dead() and sum == 3:
        #         next_alive.add(pos)
        #         changed.add((pos, True))
        #     elif cell.is_alive():
        #         changed.add((pos, False))
        #
        # for cell_pos in changed:
        #     self.__board.set_cell_value(cell_pos[0], cell_pos[1])
        #
        # next_interesting = set()
        # for pos in next_alive:
        #     for neighbour in self.__board.get_neighbours(pos):
        #         next_interesting.add(neighbour)
        # self.__interesting = next_interesting

        for i in range(self.__height):
            for j in range(self.__width):
                # TODO: перебирать не все позиции, а только интересные
                pos = Position(i, j)
                cell = self.get_cell(pos)
                if cell.is_dead() and cell.sum == 3 or cell.is_alive() and cell.sum != 2 and cell.sum != 3:
                    changed.add(pos)
        for pos in changed:
            self.get_cell(pos).invert()
        for pos in changed:
            for neighbour_pos in self.get_cell_neighbours(pos):
                self.get_cell(neighbour_pos).sum = self.__get_sum_of_neighbouring_cells(neighbour_pos)

    def add_glider(self, pos: Position):
        # TODO: обработка выхода за границы
        sz = 5
        glider = Grid.zeros_grid(sz, sz)
        glider[1][1].val = glider[2][2].val = glider[2][3].val = glider[3][1].val = glider[3][2].val = True
        self.__board[pos.x:pos.x + sz, pos.y:pos.y + sz] = glider
        for i in range(-1, sz + 1):
            for j in range(-1, sz + 1):
                nx = pos.x + i
                ny = pos.y + j
                npos = Position(nx, ny)
                if self.__is_in_board(npos):
                    self.__board[nx][ny].sum = self.__get_sum_of_neighbouring_cells(npos)

    def to_2d_array(self):
        res = np.empty([self.__height, self.__width], dtype=bool)
        for i in range(self.__height):
            for j in range(self.__width):
                res[i][j] = self.__board[i][j].val
        return res

    def clear(self):
        self.__board = Grid.zeros_grid(self.__height, self.__width)
