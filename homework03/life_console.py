import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    @staticmethod
    def draw_borders(screen) -> None:
        screen.border("|", "|", "-", "-", "+", "+", "+", "+")

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(len(self.life.curr_generation)):
            for j in range(len(self.life.curr_generation)):
                if self.life.curr_generation[i][j]:
                    screen.addstr(j + 1, i + 1, "*")
                else:
                    screen.addstr(j + 1, i + 1, " ")

    def run(self) -> None:
        screen = curses.initscr()
        running = True
        while running:
            self.draw_borders(screen)
            self.draw_grid(screen)
            running = self.life.step()
            screen.refresh()
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife(max_generations=200)
    gui = Console(game)
    gui.run()
