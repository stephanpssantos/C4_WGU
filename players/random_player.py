import random
from players.player import Player

class RandomPlayer(Player):
    def __init__(self, name):
        self.name = name

    def get_action(self, board, moves):
        columns = [i for i, v in enumerate(moves) if v == 1]
        return random.choice(columns)
    
    def early_termination(self):
        return
    
    def end_game(self, board, winner):
        return
    
    def clone(self):
        return RandomPlayer(self.name)