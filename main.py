from pettingzoo.classic import connect_four_v3
import constants
from engine.pz_game_engine import PZGameEngine
from game_controller import GameController
from players.model_player_options import ModelPlayerOptions
from players.mcts_player_options import MCTSPlayerOptions
from utilities.training_record import TrainingRecord
# from utilities.graph import load_and_graph

# Configure environment
env = connect_four_v3.env(render_mode="ansi")  #  ansi or human
env.reset(seed=constants.SEED)

# Configure player options
player0_options = ModelPlayerOptions()
player0_options.set_model_path("player_0_20240821_022149.keras")
player1_options = MCTSPlayerOptions(100)

# Configure game
engine = PZGameEngine(env)
controller = GameController(engine)
controller.set_player_0("model", player0_options)
controller.set_player_1("mcts", player1_options)
controller.set_game_limit(100000)
controller.set_win_threshold(0.5)
controller.set_save_history(True)
controller.set_track_scores(True)
controller.start_game_loop()

record = TrainingRecord()
record.make_training_record(controller)
line = record.to_string()

with open("training_records.txt", "a") as file:
    file.write(line)

# load_and_graph("ml/game_history/player0_20240819_153542.txt")