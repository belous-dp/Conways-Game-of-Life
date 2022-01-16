import random

import numpy as np

from Cell import Cell


def random_grid(height, width):
    grid = np.empty([height, width], dtype=Cell)
    for i in range(height):
        for j in range(width):
            grid[i][j] = Cell(bool(random.randint(0, 1)))
    return grid


def zeros_grid(height, width):
    grid = np.empty([height, width], dtype=Cell)
    for i in range(height):
        for j in range(width):
            grid[i][j] = Cell()
    return grid
