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
    if direction  == 0:
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
                
                
    if random_exit:
        start = (0, randint(0, rows - 1))
        finish = (randint(0, rows - 1), 0)
    else:
        start = (0, rows - 1)
        finish = (cols - 1, 0)


    grid[start[0]][start[1]] = "X"
    grid[finish[0]][finish[1]] = "X"

    for currenty in range(1, rows, 2):
        for currentx in range(1, cols, 2):
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

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """

    exits = []
    
    for y in range(len(grid)):
        if "X" == grid[y][0]:
            exits.append((y, 0))
            
    for x in range(len(grid)):
        if "X" == grid[0][x]:
            exits.append((0, x))
            
    return sorted(exits)


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
    
    k = int(grid[currentcell[0]][currentcelld[1]])
    (row, col) = currentcell
    
    if currentcell[0] != len(grid) - 1:
        
        if grid[row + 1][col] == k - 1:
            
            currentcell = (row + 1, col)
            path.append(currentcell)
            k -= 1
            
    if currentcelld[0] != 0:
        
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
        return None
    
    for i in exits:
        if encircled_exit(grid, i):
            return None
        
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
        
    return shortest_path(grid, finish)


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
    print(pd.DataFrame(MAZE))
