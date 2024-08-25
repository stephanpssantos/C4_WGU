from players.better_random_player import BetterRandomPlayer
from players.mcts_player import MCTSPlayer
from players.model_player import ModelPlayer
from players.random_player import RandomPlayer

def PlayerFactory(player_number, player_type, type_options = None):
    name = "player_0" if player_number == 0 else "player_1"

    # this should just be the else statement in the future
    if player_type == "model":
        player = ModelPlayer(name, type_options)
    elif player_type == "mcts":
        player = MCTSPlayer(name, type_options)
    elif player_type == "better_random":
        player = BetterRandomPlayer(name)
    else:
        player = RandomPlayer(name)

    return player
        