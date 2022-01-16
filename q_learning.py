import numpy as np


def Q_learning(env, episodes, discount=1.0, learing_rate=0.6, epsilon=0.2):

    Q_table = env.init_Q_table()
    episode_rewards = []
    episode_lenghts = []
    path = []

    for episode in range(episodes):

        current_state = env.reset()
        t = 0
        episode_reward  = 0
        terminal = False
        while not terminal:
            t += 1
            if episode == episodes -1:
                path.append(env.get_agent_position())

            action = np.argmax(Q_table[current_state, :])
            next_state, reward, terminal = env.step(action)
            Q_table[current_state, action] = (
                (1 - learing_rate) * Q_table[current_state, action] + learing_rate * (reward + discount * max(Q_table[next_state,:]))
            )

            episode_reward += reward
            current_state = next_state

        if episode == episodes -1:
            path.append(env.get_agent_position())

        episode_rewards.append(episode_reward)
        episode_lenghts.append(t)

    return path, episode_rewards, episode_lenghts


def Q_learning_visual():
    pass


if __name__ == "__main__":

    pass
