from pettingzoo.classic import connect_four_v3
import constants
from pz_game_engine import PZGameEngine
from game_controller import GameController
from players.model_player_options import ModelPlayerOptions
from players.mcts_player_options import MCTSPlayerOptions
# from graph import load_and_graph

# Configure environment
env = connect_four_v3.env(render_mode="human")  #  ansi or human
env.reset(seed=constants.SEED)

# Configure player options
player0_options = ModelPlayerOptions()
# player0_options.set_model_path("player_0_20240819_160553.keras")
player1_options = MCTSPlayerOptions(50)

# Configure game
engine = PZGameEngine(env)
controller = GameController(engine)
controller.set_player_0("model", player0_options)
controller.set_player_1("mcts", player1_options)
controller.set_game_limit(10000)
controller.set_win_threshold(0.9)
controller.set_save_history(True)
controller.set_track_scores(True)
controller.start_game_loop()

# load_and_graph("ml/game_history/player0_20240819_153542.txt")