import json
import pathlib
import random
from pprint import pprint
from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
        self, size: tuple = (48, 64), max_generations: Optional[float] = float("inf")
    ) -> None:

        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid()
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1
        self.grid = None

    def create_grid(self, randomize=True):
        grid = [[0] * self.cols for _ in range(self.rows)]
        if randomize:
            for i in range(self.rows):
                for j in range(self.cols):
                    grid[i][j] = random.randint(0, 1)
        self.grid = grid
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        neighbours = []
        for col in range(-1, 2):
            for row in range(-1, 2):
                if self.rows > y + row >= 0 and self.cols > x + col >= 0 and (col != 0 or row != 0):
                    neighbours.append(self.curr_generation[y + row][x + col])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0] * self.cols for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.cols):
                if 1 < sum(self.get_neighbours((i, j))) < 4 and self.curr_generation[i][j] == 1:
                    new_grid[i][j] = 1
                elif sum(self.get_neighbours((i, j))) == 3 and self.curr_generation[i][j] == 0:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
        return new_grid

    def step(self) -> bool:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        return self.is_changing and not self.is_max_generations_exceed

    @property
    def is_max_generations_exceed(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    def from_file(self, filename) -> None:
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as f:
            self.curr_generation = json.load(f)

    '''def save(self, filename: str, save_name: str) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'a+') as file:
            save = json.load(file)
            save[save_name] = self.curr_generation
            json.dump(save, file)
'''
