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

        end_found = env.set_agent_position(new_position)

        env.render(f'Iteration: {iterations}')

        sleep(0.005)

        if end_found:
            print(f'Found exit in {iterations} iterations')
            sleep(3)
            sys.exit()


def q():
    env = Maze('resources/maze.txt')
    env.load_color_theme('resources/themes.json', 'prison')
    env.prepare_window(20)

    Q_table = env.init_Q_table()

    n_episodes = 1000
    max_iter_episode = 10000
    exploration_proba = 1
    exploration_decay = 0.001
    min_exploration_proba = 0.01
    gamma = 0.6
    lr = 0.1

    #print(env.get_states())

    rewards_per_episode = list()

    for e in range(n_episodes):
        current_state = env.reset()
        done = False

        total_episode_reward  = 0
        for i in range(max_iter_episode):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            action = np.argmax(Q_table[current_state, :])

            next_state, reward, done = env.step(action)
            Q_table[current_state, action] = ((1-lr) * Q_table[current_state, action] +
                                                lr*(reward + gamma * max(Q_table[next_state,:])))
            total_episode_reward = total_episode_reward + reward

            env.render(f'Episode: {e}   Iteration: {i}')
            sleep(0.001)

            if done:
                break

            current_state = next_state

        rewards_per_episode.append(total_episode_reward)

    sample = 100
    print(f'Mean reward per {sample} episodes')
    for i in range(int(n_episodes/sample)):
        print(f'{(i+1)*sample}: mean episode reward: {np.mean(rewards_per_episode[sample*i:sample*(i+1)])}')




if __name__ == "__main__":
    q()
    # env = Maze('resources/maze2.txt')

    # #print(env.get_states())
    # #print(env.get_max_posible_states())
    # print(env.init_Q_table())
