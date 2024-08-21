class MCTSPlayerOptions:
    def __init__(self, num_sims, exploration_coeff=1.4):
        self.num_simulations = num_sims
        self.exploration_coeff = exploration_coeff