import matplotlib

from FiniteRectangleBoard import FiniteRectangleBoard
from Position import Position

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Game:

    def __init__(self, board: FiniteRectangleBoard):
        self.__board = board
        self.__interesting = self.__board.get_alive_cells_position()

    def update(self, frame_num, img):
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

        for i in range(self.__board.height):
            for j in range(self.__board.width):
                pos = Position(i, j)
                cell = self.__board.get_cell(pos)
                sum = self.__board.get_sum_of_neighbours(pos)
                if cell.is_dead() and sum == 3 or cell.is_alive() and sum != 2 and sum != 3:
                    changed.add(pos)

        for pos in changed:
            self.__board.invert_cell(pos)

        img.set_data(self.__board.to_ndarray())
        return img,

    def play(self):
        fig, ax = plt.subplots()
        img = ax.imshow(self.__board.to_ndarray(), interpolation='nearest')

        ani = animation.FuncAnimation(fig, self.update, fargs=(img,),
                                      frames=10,
                                      interval=50,
                                      save_count=50)
        plt.show()
