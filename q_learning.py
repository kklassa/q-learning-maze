import numpy as np


def quality(state, action): # Q(x, u)
    pass


def reward(state, actions):
    pass


def discounted_return(t, rewards, discount):
    ret = 0
    for k in range(len(rewards)):
        ret += discount ** k * rewards[t+k+1]

def q_learning(env, episodes, discount=1.0, alpha=0.6, epsilon=0.2):


    for episode in range(episodes):

        # reset environment
        rewards = []

        reached_terminal_state = False
        t = 0
        while not reached_terminal_state:


            t += 1





if __name__ == "__main__":
    pass

