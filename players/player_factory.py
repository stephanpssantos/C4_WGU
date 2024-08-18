from players.random_player import RandomPlayer

def PlayerFactory(player_number, player_type, type_options = None):
    name = "player_0" if player_number == 0 else "player_1"

    # this should just be the else statement in the future
    # if player_type == "random":
    #     player = RandomPlayer(name)

    return RandomPlayer(name)
        