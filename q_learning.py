import imp
import numpy as np
from itertools import count
from maze import Maze


def policy(state, actions):
    pass


def discounted_expected_return(t, rewards, discount):
    ret = 0
    for k in range(len(rewards)):
        ret += discount ** k * rewards[t+k+1]

def q_learning(env, episodes, discount=1.0, learing_rate=0.6, epsilon=0.2):

    n_states = env.get_max_possible_states()
    n_actions = env.get_max_possible_actions()

    Q_table = np.zeros((n_states, n_actions))


    for episode in range(episodes):

        # reset environment
        rewards = []

        reached_terminal_state = False
        t = 0
        while not reached_terminal_state:


            t += 1





if __name__ == "__main__":

    pass
