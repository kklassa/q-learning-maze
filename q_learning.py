import numpy as np
import pygame
import sys
from time import sleep


def Q_learning(env, episodes, discount=1.0, learing_rate=0.2):

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


def Q_learning_visual(env, episodes, discount=1.0, learing_rate=0.2,
                        delay = 0.01, square_size = 20,
                        theme_file='resources/themes.json', theme_name='prison'):
    env.load_color_theme(theme_file, theme_name)
    env.prepare_window(square_size)

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if episode == episodes -1:
                path.append(env.get_agent_position())

            action = np.argmax(Q_table[current_state, :])
            next_state, reward, terminal = env.step(action)
            Q_table[current_state, action] = (
                (1 - learing_rate) * Q_table[current_state, action] + learing_rate * (reward + discount * max(Q_table[next_state,:]))
            )

            episode_reward += reward
            current_state = next_state

            env.render(f'Episode: {episode+1}     Iteration: {t}')
            sleep(delay)

        if episode == episodes -1:
            path.append(env.get_agent_position())

        episode_rewards.append(episode_reward)
        episode_lenghts.append(t)


    return path, episode_rewards, episode_lenghts
