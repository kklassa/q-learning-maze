from maze import Maze
from q_learning import Q_learning, Q_learning_visual
from plotter import plot_q_stats


def main():

    env = Maze('resources/maze3.txt')

    episodes = 100
    path, rewards, lenghts = Q_learning_visual(env, episodes, 1, 0.2, 0.00005)

    plot_q_stats(rewards, lenghts)
    env.visualize_path(path)


if __name__ == "__main__":
    main()

