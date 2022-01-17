import numpy as np

from maze import Maze
from q_learning import Q_learning, Q_learning_visual
from plotter import plot_q_stats


def main():

    env = Maze('resources/maze-16x16.txt')

    episodes = 300
    path, rewards, lenghts = Q_learning(env, episodes, 1.0, 0.6)

    sample = 100
    for i in range(int(episodes/sample)):
        print(f'Episodes {i*sample}-{(i+1)*sample} mean reward: {np.mean(rewards[i*sample:(i+1)*sample])}')

    plot_q_stats(rewards, lenghts)
    env.visualize_path(path)


if __name__ == "__main__":
    main()

