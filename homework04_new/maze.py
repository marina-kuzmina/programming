from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    currenty, currentx = coord
    cols = len(grid[0])
    direction = randint(0, 1)
    if direction == 0:
        if currenty == 1:
            if currentx != cols - 2:
                grid[currenty][currentx + 1] = " "
        else:
            grid[currenty - 1][currentx] = " "
    else:
        if currentx != cols - 2:
            grid[currenty][currentx + 1] = " "
        else:
            if currenty != 1:
                grid[currenty - 1][currentx] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for _, cell in enumerate(empty_cells):
        grid = remove_wall(grid, cell)
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """

    list1 = []
    for x, row in enumerate(grid):
        if "X" in row:
            for y, _ in enumerate(row):
                if grid[x][y] == "X":
                    list1.append((x, y))
    return list1


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """

    for row in range(len(grid) - 1):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == k:
                if grid[row + 1][col] == 0:
                    grid[row + 1][col] = k + 1
                if grid[row - 1][col] == 0:
                    grid[row - 1][col] = k + 1
                if grid[row][col + 1] == 0:
                    grid[row][col + 1] = k + 1
                if grid[row][col - 1] == 0:
                    grid[row][col - 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """

    path = [exit_coord]
    currentcell = exit_coord

    k = int(grid[currentcell[0]][currentcell[1]])
    (row, col) = currentcell

    if currentcell[0] != len(grid) - 1:
        if grid[row + 1][col] == k - 1:
            currentcell = (row + 1, col)
            path.append(currentcell)
            k -= 1
    if currentcell[0] != 0:
        if grid[row - 1][col] == k - 1:
            currentcell = (row - 1, col)
            path.append(currentcell)
            k -= 1
    if currentcell[1] != len(grid[0]) - 1:
        if grid[row][col + 1] == k - 1:
            currentcell = (row, col + 1)
            path.append(currentcell)
            k -= 1
    if currentcell[1] != 0:
        if grid[row][col - 1] == k - 1:
            currentcell = (row, col - 1)
            path.append(currentcell)
            k -= 1
    while grid[currentcell[0]][currentcell[1]] != 1:
        (row, col) = currentcell
        if grid[row + 1][col] == k - 1:
            currentcell = (row + 1, col)
            path.append(currentcell)
            k -= 1
        elif grid[row - 1][col] == k - 1:
            currentcell = (row - 1, col)
            path.append(currentcell)
            k -= 1
        elif grid[row][col + 1] == k - 1:
            currentcell = (row, col + 1)
            path.append(currentcell)
            k -= 1
        elif grid[row][col - 1] == k - 1:
            currentcell = (row, col - 1)
            path.append(currentcell)
            k -= 1
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """

    if coord[0] == 0 and grid[coord[0] + 1][coord[1]] != " ":
        return True

    if coord[1] == 0 and grid[coord[0]][coord[1] + 1] != " ":
        return True

    if coord[0] == len(grid) - 1 and grid[coord[0] - 1][coord[1]] != " ":
        return True

    if coord[1] == len(grid[0]) - 1 and grid[coord[0]][coord[1] - 1] != " ":
        return True

    return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) == 1:
        return (grid, None)

    for i in exits:
        if encircled_exit(grid, i):
            return (grid, None)

    start = exits[0]
    finish = exits[1]

    grid[start[0]][start[1]] = 1

    for row in range(len(grid) - 1):
        for col in range(len(grid[row]) - 1):
            if grid[row][col] == " ":
                grid[row][col] = 0

    grid[finish[0]][finish[1]] = 0

    k = 1

    if start[0] != len(grid) - 1:
        if grid[start[0] + 1][start[1]] == 0:
            grid[start[0] + 1][start[1]] = k + 1

    if start[0] != 0:
        if grid[start[0] - 1][start[1]] == 0:
            grid[start[0] - 1][start[1]] = k + 1

    if start[1] != len(grid[0]) - 1:
        if grid[start[0]][start[1] + 1] == 0:
            grid[start[0]][start[1] + 1] = k + 1

    if start[1] != 0:
        if grid[start[0]][start[1] - 1] == 0:
            grid[start[0]][start[1] - 1] = k + 1

    while grid[finish[0]][finish[1]] == 0:
        k += 1
        make_step(grid, k)

    #return shortest_path(grid, finish)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))  # D, path1)
    print(pd.DataFrame(MAZE))
