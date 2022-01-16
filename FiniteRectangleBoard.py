import numpy as np

import Grid
from BoardInterface import BoardInterface
from Cell import Cell
from Position import Position


class FiniteRectangleBoard(BoardInterface):
    default_size = 100
    __NUM_DIRS = 8  # количество направлений, куда можем перейти
    __dx = [-1, -1, -1, 0, 1, 1, 1, 0]  # массивы для переходов в соседние клетки
    __dy = [-1, 0, 1, 1, 1, 0, -1, -1]

    def __init__(self, height: int = default_size, width: int = default_size):
        self.__height = height
        self.__width = width
        self.__board = Grid.random_grid(height, width)  # генерируем случайную доску
        # На не очень хаотичных паттернах получается, что по большому количеству точек пробегаемся зря,
        # поэтому можем рассматривать только интересные позиции -- те, вокруг которых ситуация изменилась.
        # Тогда значение в этих клетках, возможно, обновится.
        # В начале пометим всё поле как интересное, потому что не жалко, т.к. "лишние" клетки уйдут после первого шага
        self.__interesting = set()  # сохраним сюда интересные позиции
        for i in range(self.__height):
            for j in range(self.__width):
                pos = Position(i, j)
                self.__update_sum(pos)
                self.__interesting.add(pos)

    def get_cell(self, pos: Position) -> Cell:
        return self.__board[pos.x][pos.y]

    # На самом деле я не знаю, зачем этот метод, потому что я его в коде не использую
    def set_cell(self, pos: Position, cell: Cell):
        self.__board[pos.x][pos.y] = cell
        self.__interesting.add(pos)  # добавим в интересные позиции обновившуюся клетку и её соседей
        self.__interesting.update(self.get_neighbours(pos))

    def get_neighbours(self, pos: Position) -> list[Position]:
        res = []
        for i in range(self.__NUM_DIRS):
            neighbour = Position(pos.x + self.__dx[i], pos.y + self.__dy[i])
            if self.__is_in_board(neighbour):
                res.append(neighbour)
        return res

    def __is_in_board(self, pos: Position):
        return 0 <= pos.x < self.__height and 0 <= pos.y < self.__width

    def __get_sum_of_neighbouring_cells(self, pos: Position) -> int:
        res = 0
        for neighbour in self.get_neighbours(pos):
            if self.__board[neighbour.x][neighbour.y].is_alive():
                res += 1
        return res

    # Обновляет, сколько живых соседей есть у клетки
    def __update_sum(self, pos: Position):
        self.get_cell(pos).sum = self.__get_sum_of_neighbouring_cells(pos)

    # Делает переход от текущего состояния к следующему
    def make_move(self):
        changed = set()  # запоминаем клетки, в которых что-то изменилось
        for pos in self.__interesting:
            cell = self.get_cell(pos)
            # Тут переходим по правилам:
            # 1. Any live cell with two or three live neighbours survives.
            # 2. Any dead cell with three live neighbours becomes a live cell.
            # 3. All other live cells die in the next generation. Similarly, all other dead cells stay dead.
            if cell.is_dead() and cell.sum == 3 or cell.is_alive() and cell.sum != 2 and cell.sum != 3:
                changed.add(pos)

        # Долгий 2d цикл
        # for i in range(self.__height):
        #     for j in range(self.__width):
        #         pos = Position(i, j)
        #         cell = self.get_cell(pos)
        #         if cell.is_dead() and cell.sum == 3 or cell.is_alive() and cell.sum != 2 and cell.sum != 3:
        #             changed.add(pos)

        # Меняем значение клеток. Сразу это делать нельзя, потому что тогда старые и новые состояния перемешаются.
        for pos in changed:
            self.get_cell(pos).invert()

        # Пересчитываем количество живых соседей и сохраняем, какие клетки будут интересны дальше
        next_interesting = set()
        for pos in changed:
            self.__update_sum(pos)
            next_interesting.add(pos)
            for neighbour in self.get_neighbours(pos):
                self.__update_sum(neighbour)
                next_interesting.add(neighbour)
        self.__interesting = next_interesting

    # Создаёт планер в указанной позиции
    def add_glider(self, pos: Position):
        sz = 5
        glider = Grid.zeros_grid(sz, sz)
        # Ещё одна порция минусов от требования вынести Клетку в отдельный класс по принципам ООП: здесь нет возможности
        # понять, как выглядит фигура, не загуглив или не запустив код. А если не выносить клетку в отдельный класс,
        # можно было бы задавать более наглядно:
        # [[0, 0, 0, 0, 0],
        #  [0, 1, 0, 0, 0],
        #  [0, 0, 1, 1, 0],
        #  [0, 1, 1, 0, 0]
        #  [0, 0, 0, 0, 0]]
        glider[1][1].val = glider[2][2].val = glider[2][3].val = glider[3][1].val = glider[3][2].val = True
        self.__pattern_update(pos, sz, sz, glider, "glider")

    # Создаёт ружьё Госпера в указанной позиции
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
        self.__pattern_update(pos, h, w, gun, "Gosper glider gun")

    # Сливает наш паттерн с основным полем. Если выходим за границы -- обрезаем. Если совсем выходим -- игнорируем.
    def __pattern_update(self, pos, h, w, pattern, pattern_name=""):
        if pos.x < 0 or pos.x >= self.__height or pos.y < 0 or pos.y >= self.__width:  # всё плохо
            print(f"Warning: pattern {pattern_name} [{h}, {w}] at pos [{pos.x}, {pos.y}] is outside the board ",
                  f"[{self.__height}, {self.__width}], so it was ignored", sep='')
            return
        if pos.x + h > self.__height or pos.y + w > self.__width:  # всё не очень плохо
            print(f"Warning: pattern {pattern_name} [{h}, {w}] at pos [{pos.x}, {pos.y}] was trimmed to board size ",
                  f"[{self.__height}, {self.__width}]", sep='')
        self.__board[pos.x:pos.x + h, pos.y:pos.y + w] = \
            pattern[:min(h, self.__height - pos.x), :min(w, self.__width - pos.y)]
        # Пройдёмся по тому куску, который обновили, и соседним клеткам. Пересчитаем количество живых и интересных.
        for i in range(-1, h + 1):
            for j in range(-1, w + 1):
                cur_pos = Position(pos.x + i, pos.y + j)
                if self.__is_in_board(cur_pos):
                    self.__update_sum(cur_pos)
                    self.__interesting.add(cur_pos)

    # Костыль из-за вынесения Cell в отдельный класс. Matplotlib не умеет рисовать таблички из Cell, а вот из bool умеет
    def to_2d_array(self):
        res = np.empty([self.__height, self.__width], dtype=bool)
        for i in range(self.__height):
            for j in range(self.__width):
                res[i][j] = self.__board[i][j].val
        return res

    def clear(self):
        self.__board = Grid.zeros_grid(self.__height, self.__width)
