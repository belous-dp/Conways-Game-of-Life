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

    def __update_sum(self, pos: Position):
        self.get_cell(pos).sum = self.__get_sum_of_neighbouring_cells(pos)

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
            self.__update_sum(pos)
            for neighbour_pos in self.get_cell_neighbours(pos):
                self.__update_sum(neighbour_pos)

    def add_glider(self, pos: Position):
        # TODO: обработка выхода за границы
        sz = 5
        glider = Grid.zeros_grid(sz, sz)
        glider[1][1].val = glider[2][2].val = glider[2][3].val = glider[3][1].val = glider[3][2].val = True
        self.__pattern_update(pos, sz, sz, glider)

    def add_gosper_glider_gun(self, pos: Position):
        h = 11
        w = 38
        gun = Grid.zeros_grid(h, w)
        gun[5][1].val = gun[6][1].val = gun[5][2].val = gun[6][2].val = True
        gun[5][11].val = gun[6][11].val = gun[7][11].val = True
        gun[4][12].val = gun[8][12].val = True
        gun[3][13].val = gun[9][13].val = True
        gun[3][14].val = gun[9][14].val = True
        gun[6][15].val = True
        gun[4][16].val = gun[8][16].val = True
        gun[5][17].val = gun[6][17].val = gun[7][17].val = True
        gun[6][18].val = True
        gun[3][21].val = gun[4][21].val = gun[5][21].val = True
        gun[3][22].val = gun[4][22].val = gun[5][22].val = True
        gun[2][23].val = gun[6][23].val = True
        gun[1][25].val = gun[2][25].val = gun[6][25].val = gun[7][25].val = True
        gun[3][35].val = gun[4][35].val = gun[3][36].val = gun[4][36].val = True
        self.__pattern_update(pos, h, w, gun)

    def __pattern_update(self, pos, h, w, pattern):
        self.__board[pos.x:pos.x + h, pos.y:pos.y + w] = pattern
        for i in range(-1, h + 1):
            for j in range(-1, w + 1):
                cur_pos = Position(pos.x + i, pos.y + j)
                if self.__is_in_board(cur_pos):
                    self.__update_sum(cur_pos)

    def to_2d_array(self):
        res = np.empty([self.__height, self.__width], dtype=bool)
        for i in range(self.__height):
            for j in range(self.__width):
                res[i][j] = self.__board[i][j].val
        return res

    def clear(self):
        self.__board = Grid.zeros_grid(self.__height, self.__width)
