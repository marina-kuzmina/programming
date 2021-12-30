import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(
        self,
        life: GameOfLife,
        cell_size: int = 10,
        speed: int = 10,
        width: int = 640,
        height: int = 480,
    ) -> None:
        super().__init__(life)
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

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if self.life.curr_generation[i][j]:
                    color = "green"
                else:
                    color = "white"
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size),
                )

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        pause = False
        while running:
            if not pause:
                running = self.life.step()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = event.pos
                    x, y = mouse_pos
                    self.life.curr_generation[y // self.cell_size][x // self.cell_size] = 1
                    self.draw_grid()
                    pygame.display.flip()
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    game = GameOfLife # (randomize=True)
    gui = GUI(game)
    gui.run()
