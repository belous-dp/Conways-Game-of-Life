import argparse

from FiniteRectangleBoard import FiniteRectangleBoard
from Game import Game
from Position import Position


def main():
    # TODO: комментарии
    # TODO: сохранение анимации
    # TODO: скорость анимации

    # чтобы было удобнее парсить аргументы из командной строки, используем argparse
    parser = argparse.ArgumentParser(description="Выполняет игру Жизнь, по умолчанию поле генерируется случайным. "
                                                 "При добавлении каких-то паттернов поле генерируется пустым")
    parser.add_argument('--width', type=int, default=100, help='ширина поля')
    parser.add_argument('--height', type=int, default=100, help='высота поля')
    parser.add_argument('--glider', action='store_true', help='добавлять ли планер на позицию (0, 0)')
    parser.add_argument('--add-glider', nargs=2, type=int, action='append', default=[], dest='gliders',
                        help='добавить планер на заданную позицию')
    parser.add_argument('--gosper-glider-gun', action='store_true',
                        help='добавлять ли планерное ружьё Госпера на позицию (0, 0)')
    # TODO: паттерн больше размера поля
    # TODO: импорт паттернов
    args = parser.parse_args()
    board = FiniteRectangleBoard(args.height, args.width)
    if args.glider:
        args.gliders.append([0, 0])
    if args.gliders or args.gosper_glider_gun:
        board.clear()
    for pos in args.gliders:
        board.add_glider(Position(pos[0], pos[1]))
    if args.gosper_glider_gun:
        board.add_gosper_glider_gun(Position(0, 0))
    game = Game(board)
    game.play()


if __name__ == '__main__':
    main()
