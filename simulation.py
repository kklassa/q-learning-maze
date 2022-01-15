import numpy as np
import pygame
import sys
from time import sleep

from maze import Maze


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
            prob.append(1.5)
        elif board[row][col] == 1:
            prob.append(1)
        else:
            prob.append(0)
    prob[min_index] = 1.6
    sum = np.sum(prob)
    prob = [p / sum for p in prob]

    return moves[np.random.choice(moves.shape[0], 1, p=prob), :].flatten()


def main():

    env = Maze('resources/maze3.txt')
    env.load_color_theme('resources/themes.json', 'prison')
    env.prepare_window(20)

    iterations = 0
    end_found = False
    while not end_found:
        iterations += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        actions = env.get_actions()
        new_position = actions[np.random.randint(actions.shape[0], size=1), :].flatten()

        result = env.set_agent_position(new_position)

        env.render(f'Iteration: {iterations}')

        sleep(0.005)

        if result:
            print(f'Found exit in {iterations} iterations')
            end_found = True
            sleep(3)
            sys.exit()


if __name__ == "__main__":
    main()
