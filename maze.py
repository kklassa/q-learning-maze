import numpy as np


def prepare_maze(filepath):
    maze = []
    rows = 0
    with open(filepath, 'r') as fh:
        for line in fh:
            row = [character for character in line if character != '\n']
            if row:
                rows +=1
            maze.append(row)
    columns = len(maze[0])

    maze_board = np.zeros((rows, columns))

    for row_idx in range(rows):
        for column_idx in range(columns):
            char = maze[row_idx][column_idx]
            if char == '.':
                maze_board[row_idx][column_idx] = 0
            elif char =='#':
                maze_board[row_idx][column_idx] = 1
            elif char == 'S':
                maze_board[row_idx][column_idx] = 5
                start = np.array([row_idx, column_idx])
            elif char == 'F':
                maze_board[row_idx][column_idx] = 10
                end = np.array([row_idx, column_idx])

    return maze_board, start, end
