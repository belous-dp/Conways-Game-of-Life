from BoardInterface import BoardInterface

import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Game:

    def __init__(self, board: BoardInterface):
        self.__board = board

    # Обновляет кадр
    def __update(self, frame_num, img):
        self.__board.make_move()
        img.set_data(self.__board.to_2d_array())
        return img

    def play(self):
        fig, ax = plt.subplots()
        img = ax.imshow(self.__board.to_2d_array())
        ani = animation.FuncAnimation(fig, self.__update, fargs=(img,), interval=50)
        plt.show()
