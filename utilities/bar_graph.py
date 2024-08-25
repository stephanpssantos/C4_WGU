import matplotlib.pyplot as plt
import pandas as pd

session_times = {
    'DQN vs MCTS 25': ('2024-08-20 19:21:54.942147', '2024-08-20 19:24:29.154896'),
    'DQN vs MCTS 50': ('2024-08-20 19:29:02.227896', '2024-08-20 20:12:51.453876'),
    'DQN vs MCTS 100': ('2024-08-20 21:01:45.786125', '2024-08-21 02:21:49.557316'),
}

session_times = {k: (pd.to_datetime(v[0]), pd.to_datetime(v[1])) for k, v in session_times.items()}

durations = {k: (v[1] - v[0]).seconds for k, v in session_times.items()}

fig, ax = plt.subplots()
bars = ax.bar(durations.keys(), durations.values(), color='skyblue')

ax.set_xlabel('Training session')
ax.set_ylabel('Duration (seconds)')
ax.set_title('Training session duration between different rollout limits')

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), 
            ha='center', va='bottom')

# Display the plot
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()