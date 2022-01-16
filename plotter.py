from matplotlib import pyplot as plt


def plot_q_stats(rewards, lenghts, r_color = 'red', l_color = 'green'):
    episodes = range(len(rewards))


    plt.subplot(1, 2, 1)
    plt.title('rewards per episode')
    plt.xlabel('episodes')
    plt.ylabel('rewards')
    plt.plot(episodes, rewards, '-', color=r_color)

    plt.subplot(1, 2, 2)
    plt.title('lenghts per episode')
    plt.xlabel('episodes')
    plt.ylabel('lenghts')
    plt.plot(episodes, lenghts, '-', color=l_color)

    plt.show()
