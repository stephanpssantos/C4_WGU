class MCTSPlayerOptions:
    def __init__(self, num_sims, clone_level=0, exploration_coeff=2):
        self.num_simulations = num_sims
        self.exploration_coeff = exploration_coeff
        self.clone_level = clone_level