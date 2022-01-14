from os import stat
from turtle import pos
import numpy as np
import pygame
import sys
from time import sleep
import json

from maze import prepare_maze



def draw_maze(board, square_size, color_theme):
    rows, columns = board.shape
    height = rows * square_size
    width = columns * square_size
    screen = pygame.display.set_mode((width, height))
    screen.fill(color_theme['floor_color'])

    return screen

def update_maze(screen, board, square_size, color_theme):
    screen.fill(color_theme['floor_color'])
    for row in range(board.shape[0]):
        for col in range(board.shape[1]):
            square = board[row][col]
            if square:
                points = [
                    (col * square_size, row * square_size),
                    (col * square_size + square_size, row * square_size),
                    (col * square_size + square_size, row * square_size + square_size),
                    (col * square_size, row * square_size + square_size),
                ]
                if square == 1:
                    square_color = color_theme['wall_color']
                elif square == 5:
                    square_color = color_theme['position_color']
                elif square == 10:
                    square_color = color_theme['end_color']
                elif square == 4:
                    square_color = color_theme['visited_color']
                pygame.draw.polygon(screen, square_color, points)

    return screen

def available_moves(board, position):
    max_row, max_col = board.shape
    offsets = [-1, 0, 1]
    available_positions = []
    for row_off in offsets:
        for col_off in offsets:
            row = position[0] + row_off
            col = position[1] + col_off
            if row >= 0 and col >= 0 and row < max_row and col < max_col and not (row == position[0] and col == position[1]):
                if board[row][col] != 1:
                    available_positions.append((row, col))
    return np.array(available_positions)

def euclidean_heuristic(board, moves, end):
    prob = []
    end_row, end_col = end
    min_distance = float('inf')
    min_index = None
    for index in range(moves.shape[0]):
        row, col = moves[index]
        distance = np.sqrt(np.power(end_row - row, 2) + np.power(end_col - col, 2))
        if min_distance > distance:
            min_index = index
        if board[row][col] == 0:
            prob.append(2)
        elif board[row][col] == 4:
            prob.append(1)
        else:
            prob.append(0)
    prob[min_index] = 3
    sum = np.sum(prob)
    prob = [p / sum for p in prob]

    return moves[np.random.choice(moves.shape[0], 1, p=prob), :].flatten()

def calculate_rewards(moves, board):
    pass


def main():



    filepath = 'resources/maze.txt'
    with open('resources/themes.json') as fh:
        themes = json.load(fh)

    color_theme = themes['pastel'][0]

    pygame.init()
    maze, start, end = prepare_maze(filepath)
    square_size = 20
    screen = draw_maze(maze, square_size, color_theme)
    update_maze(screen, maze, square_size, color_theme)

    pygame.display.set_caption('maze')

    position = start
    iterations = 0
    sim_over = False
    while not sim_over:
        iterations += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        row, col = position
        maze[row][col] = 4 # mark as visited
        av_pos = available_moves(maze, position)
        # new_position = av_pos[np.random.randint(av_pos.shape[0], size=1), :].flatten()
        new_position = euclidean_heuristic(maze, av_pos, end)
        row, col = new_position
        maze[row][col] = 5

        print(f'Position: {position}\nChosen next move: {new_position}\nIteration: {iterations}')
        position = new_position

        update_maze(screen, maze, square_size, color_theme)

        sleep(0.01)
        pygame.display.update()

        if (position==end).all():
            print(f'Found exit in {iterations} iterations')
            sleep(3)
            sys.exit()


if __name__ == "__main__":
    main()
