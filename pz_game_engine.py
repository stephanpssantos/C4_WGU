from game_engine import GameEngine

class PZGameEngine(GameEngine):
    def __init__(self, env):
        super().__init__()
        self.env = env

    def start_game(self):
        for agent in self.env.agent_iter():
            player = self.player1 if self.next_player else self.player0
            self.next_player = not self.next_player

            if self.game_over():
                action = None
            else:
                action = player.get_action(self.get_board(), self.get_moves())

            self.env.step(action)
        pass

    def reset(self):
        self.env.reset()

    def get_moves(self):
        columns = self.env.last()[0]["action_mask"]
        return [i for i, v in enumerate(columns) if v == 1]
    
    def get_board(self):
        return self.env.last()[0]["observation"]
    
    def game_over(self):
        termination, truncation = self.env.last()[2:4]
        return True if termination or truncation else False
    
    def end_game(self):
        self.env.close()