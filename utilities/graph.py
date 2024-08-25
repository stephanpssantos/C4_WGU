import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

file_path = Path(__file__).parent.parent / "ml" / "game_history" / "player0_20240823_014258.txt"
point_history = np.loadtxt(file_path)
lower_limit = 0
upper_limit = len(point_history)

# window_size = (upper_limit * 10) // 100
window_size = 1000

plot_rolling_mean_only = False
plot_data_only = False

points = point_history[lower_limit:upper_limit]

# Generate x-axis for plotting.
episode_num = [x for x in range(lower_limit, upper_limit)]

# Use Pandas to calculate the rolling mean (moving average).
rolling_mean = pd.DataFrame(points).rolling(window_size).mean()

plt.figure(figsize=(10, 7), facecolor="white")

if plot_data_only:
    plt.plot(episode_num, points, linewidth=1, color="cyan")
elif plot_rolling_mean_only:
    plt.plot(episode_num, rolling_mean, linewidth=2, color="magenta")
else:
    plt.plot(episode_num, points, linewidth=1, color="cyan", alpha=0)
    plt.plot(episode_num, rolling_mean, linewidth=2, color="magenta")

text_color = "black"

ax = plt.gca()
ax.set_facecolor("black")
ax.set_title("DQN vs 1000 rollout MCTS")
plt.grid()
plt.xlabel("Games played", color=text_color, fontsize=30)
plt.ylabel("Wins / 1000 games", color=text_color, fontsize=30)
yNumFmt = mticker.StrMethodFormatter("{x:,}")
ax.yaxis.set_major_formatter(yNumFmt)
ax.tick_params(axis="x", colors=text_color)
ax.tick_params(axis="y", colors=text_color)
plt.show()