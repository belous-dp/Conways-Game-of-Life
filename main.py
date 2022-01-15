from FiniteRectangleBoard import FiniteRectangleBoard
from Game import Game


def main():
    board = FiniteRectangleBoard(80, 80)
    game = Game(board)
    game.play()


if __name__ == '__main__':
    main()
