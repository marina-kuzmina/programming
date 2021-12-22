import random
from copy import copy
from pprint import pprint

import json
import pathlib

from typing import List, Tuple

import pygame

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 5) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = [[0] * (self.width // self.cell_size) for _ in range(self.height // self.cell_size)]

    def draw_lines(self) -> None:
        # @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        running = True
        self.grid = self.create_grid(randomize=True)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.grid = self.get_next_generation()
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False):
        if randomize:
            for i in range(self.height // self.cell_size):
                for j in range(self.width // self.cell_size):
                    self.grid[i][j] = random.randint(0, 1)
        return self.grid

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.grid[i][j]:
                    color = "green"
                else:
                    color = "white"
                pygame.draw.rect(self.screen, pygame.Color(color),
                                 (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        neighbours = []
        for col in range(-1, 2):
            for row in range(-1, 2):
                if self.height // self.cell_size > x + col >= 0 and self.width // self.cell_size > y + row >= 0 and (
                        col != 0 or row != 0):
                    neighbours.append(self.grid[x + col][y + row])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = [[0 for _ in range(8)] for _ in range(6)]
        for i in range(self.height // self.cell_size):
            for j in range(self.width // self.cell_size):
                if 1 < sum(self.get_neighbours((i, j))) < 4 and self.grid[i][j] == 1:
                    new_grid[i][j] = 1
                elif sum(self.get_neighbours((i, j))) == 3 and self.grid[i][j] == 0:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
        return new_grid

    def from_file(self, filename) -> None:
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename) as file:
            self.grid = json.load(file)

    def save(self, filename: str, save_name: str) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, 'a+') as file:
            save = json.load(file)
            save[save_name] = self.grid
            json.dump(save, file)


if __name__ == '__main__':
    game = GameOfLife(320, 240, 40)
    game.run()
