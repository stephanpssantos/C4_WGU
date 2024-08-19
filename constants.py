# Hyperparameters
SEED = 42  # Seed for the pseudo-random number generator.
MINIBATCH_SIZE = 100  # Mini-batch size.
MEMORY_SIZE = 100_000_000  #  size of memory buffer
ALPHA = 1e-5  #  learning rate  
EPSILON = 1.0  #  initial ε value for ε-greedy policy
E_DECAY = 0.995  # ε-decay rate for the ε-greedy policy.
E_MIN = 0.05  # Minimum ε value for the ε-greedy policy.
GAMMA = 0.9  #  discount factor
TAU = 1e-3  # Soft update parameter.

# Environment details
STATE_SIZE = (6,7,2)
NUM_ACTIONS = 7

# Game details
GAME_COUNT_AVERAGE = 1000 # check last x number of games when getting performance average