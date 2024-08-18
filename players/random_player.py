import random
from players.player import Player

class RandomPlayer(Player):
    def __init__(self, name):
        self.name = name

    def get_action(self, board, moves):
        columns = [i for i, v in enumerate(moves) if v == 1]
        return random.choice(columns)
    
    def end_game(self, board, winner):
        return