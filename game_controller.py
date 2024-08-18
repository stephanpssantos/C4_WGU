from players.player_factory import PlayerFactory

class GameController:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_number = 0
        self.game_history = []
        pass

    def set_players(self, player0, player1):
        self.player0 = PlayerFactory(0, player0)
        self.player1 = PlayerFactory(1, player1)
        return
    
    def set_game_limit(self, limit):
        self.game_limit = limit
    
    def start_game_loop(self):
        self._startup_check()
        
        while (self.game_number < self.game_limit):
            self._start_new_game()

        self.game_engine.end_game()
        pass

    def _start_new_game(self):
        if self.game_number >= self.game_limit: 
            return
        
        self.game_number += 1
        self.game_engine.reset()
        result = self.game_engine.start_game()
        self.game_history.append(result)
        return

    def _startup_check(self):
        if self.game_limit is None:
            self.game_limit = 1

        if self.game_engine.player0 is None:
            self.game_engine.player0 = PlayerFactory(0, "random")
        
        if self.game_engine.player1 is None:
            self.game_engine.player1 = PlayerFactory(1, "random")
