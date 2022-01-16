import argparse

from FiniteRectangleBoard import FiniteRectangleBoard
from Game import Game
from Position import Position


def main():
    # TODO: комментарии
    # TODO: сохранение анимации
    # TODO: скорость анимации

    # чтобы было удобнее парсить аргументы из командной строки, используем argparse
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life simulation. The field is empty if any "
                                                 "optional patterns were given. Otherwise the field is random")
    parser.add_argument('--width', type=int, default=100, help='width of the field')
    parser.add_argument('--height', type=int, default=100, help='height of the field')
    parser.add_argument('--glider', action='store_true', help='creates glider at position (0, 0)')
    parser.add_argument('--add-glider', nargs=2, type=int, action='append', default=[], dest='gliders',
                        help='creates glider at the specified position', metavar='POSITION')
    parser.add_argument('--gosper-glider-gun', action='store_true',
                        help='creates Gosper glider gun at position (0, 0)')
    parser.add_argument('--add-gosper-glider-gun', nargs=2, type=int, action='append', default=[], dest='ggguns',
                        help='creates Gosper glider gun at the specified position', metavar='POSITION')
    # TODO: импорт паттернов
    args = parser.parse_args()
    if args.height <= 0 or args.width <= 0:
        print(f"Warning: invalid field size: [{args.height}, {args.width}]. The default value will be used.")
    board = FiniteRectangleBoard(args.height, args.width)
    if args.glider:
        args.gliders.append([0, 0])
    if args.gosper_glider_gun:
        args.ggguns.append([0, 0])
    if args.gliders or args.ggguns:
        board.clear()
    for pos in args.gliders:
        board.add_glider(Position(pos[0], pos[1]))
    for pos in args.ggguns:
        board.add_gosper_glider_gun(Position(pos[0], pos[1]))
    game = Game(board)
    game.play()


if __name__ == '__main__':
    main()
