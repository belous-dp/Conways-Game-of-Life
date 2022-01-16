import argparse

from FiniteRectangleBoard import FiniteRectangleBoard
from Game import Game
from Position import Position


def main():
    # чтобы было удобнее парсить аргументы из командной строки, используем argparse
    parser = argparse.ArgumentParser(description="Выполняет игру Жизнь")
    parser.add_argument('--width', type=int, default=100, help='ширина поля')
    parser.add_argument('--height', type=int, default=100, help='высота поля')
    parser.add_argument('--add-glider', action='store_true', help='добавлять ли планер на позицию (0, 0)')
    args = parser.parse_args()
    board = FiniteRectangleBoard(width=args.width, height=args.height)
    if args.add_glider:
        board.clear()
        board.add_glider(Position(0, 0))
    game = Game(board)
    game.play()


if __name__ == '__main__':
    main()
