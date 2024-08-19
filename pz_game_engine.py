import constants
from game_engine import GameEngine

class PZGameEngine(GameEngine):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.post_game_done = False
        self.winner = None

    def start_game(self):
        for agent in self.env.agent_iter():
            player = self.player1 if self.next_player else self.player0
            self.next_player = not self.next_player

            if self.game_over():
                action = None
                self._post_game(player)
            else:
                action = player.get_action(self.get_board(), self.get_moves())

            self.env.step(action)
        
        return self.winner

    def reset(self):
        self.next_player = 0
        self.post_game_done = False
        self.winner = None
        self.env.reset(constants.SEED)

    def get_moves(self):
        return self.env.last()[0]["action_mask"]
    
    def get_board(self):
        return self.env.last()[0]["observation"]
    
    def game_over(self):
        termination, truncation = self.env.last()[2:4]
        return True if termination or truncation else False
    
    def early_termination(self):
        self.player0.early_termination()
        self.player1.early_termination()
    
    def end_game(self):
        self.env.close()
    
    def _post_game(self, player):
        if self.post_game_done: return
        winner = self._check_winner()
        player.end_game(self.get_board(), winner)
        next_player = self.player1 if self.next_player else self.player0
        next_player.end_game(self.get_board(), winner)
        self.post_game_done = True
        self.winner = winner
        return

    def _check_winner(self):
        winner = self.player1 if self.next_player else self.player0
        reward = self.env.last()[1]
        return "draw" if reward == 0 else winner.name