import matplotlib.pyplot as plt
from collections import Counter
from pathlib import Path

def count_values(filename):
    counts = Counter()
    with open(filename, 'r') as file:
        for line in file:
            values = line.split()
            for value in values:
                try:
                    num = int(value)
                    if num in (-1, 0, 1):
                        counts[num] += 1
                except ValueError:
                    continue
    return counts

file_path = Path(__file__).parent.parent / "ml" / "game_history" / "player0_20240824_211956.txt"

counts = count_values(file_path)

labels = ['Lost', 'Draw', 'Won']
sizes = [counts.get(-1, 0), counts.get(0, 0), counts.get(1, 0)]
colors = ['lightcoral', 'lightgrey', 'lightblue']
explode = (0.1, 0, 0)  # explode the 1's slice slightly

fig, ax = plt.subplots()
ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
       shadow=True, startangle=140)

ax.axis('equal')

plt.title('DQN win distribution vs other DQN')

plt.show()