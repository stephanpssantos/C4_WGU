from pettingzoo.classic import connect_four_v3
import constants
from pz_game_engine import PZGameEngine
from game_controller import GameController
from players.model_player_options import ModelPlayerOptions
# from graph import load_and_graph

# Configure environment
env = connect_four_v3.env(render_mode="ansi")  #  ansi or human
env.reset(seed=constants.SEED)

# Configure player options
model_player_options = ModelPlayerOptions()
# model_player_options.set_model_path("player_0_20240819_160553.keras")

# Configure game
engine = PZGameEngine(env)
controller = GameController(engine)
controller.set_player_0("model", model_player_options)
controller.set_player_1("random")
controller.set_game_limit(100000)
controller.set_win_threshold(0.9)
controller.set_save_history(True)
controller.start_game_loop()

# load_and_graph("ml/game_history/player0_20240819_153542.txt")

# TODO
# create an mcts player
# create a sim_game_engine class
# separate load_and_graph into its own startup file?