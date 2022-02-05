# Conway's Game of Life
Реализация [игры Жизнь](https://en.wikipedia.org/wiki/Conway's_Game_of_Life).

Если никаких параметров передано не было, генерирует случайное поле. Иначе генерирует чистое поле с теми объектами, которые были указаны в качестве аргументов.

## Использование
Для запуска нужен python 3.10, numpy, matplotlib.

Запуск: `python main.py [аргументы]`.

Options:
  * `-h`, `--help`            помощь
  * `--width WIDTH`         ширина поля
  * `--height HEIGHT`       высота поля
  * `--glider`              создаёт планер на позиции (0, 0)
  * `--add-glider POS_X POS_Y`
                        создаёт планер на указанной позиции
  * `--gosper-glider-gun`   создаёт ружьё Госпера на позиции (0, 0)
  * `--add-gosper-glider-gun POS_X POS_Y`
                        создаёт ружьё Госпера на указанной позиции

Все аргументы кроме `--width` и `--height` могут быть указаны несколько раз для добавления нескольких объектов одного типа.

Пример: `python main.py --width 80 --height 80 --add-glider 5 5 --add-glider 10 30 --add-glider 30 10` 
