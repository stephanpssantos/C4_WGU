import random
from players.player import Player

class RandomPlayer(Player):
    def __init__(self, name):
        self.name = name

    def get_action(self, board, moves):
        return random.choice(moves)