from pettingzoo.classic import connect_four_v3
import constants
from engine.pz_game_engine import PZGameEngine
from game_controller import GameController
from players.model_player_options import ModelPlayerOptions
from players.mcts_player_options import MCTSPlayerOptions
from utilities.training_record import TrainingRecord

# Configure environment
env = connect_four_v3.env(render_mode="ansi")  #  ansi or human
env.reset(seed=constants.SEED)

# Configure player options
player0_options = ModelPlayerOptions()
player0_options.set_model_path("player_0_20240824_043123.keras")
player1_mcts_options = MCTSPlayerOptions(1000)
player1_model_options = ModelPlayerOptions()
player1_model_options.set_model_path("player_1_20240824_121714.keras")
# player1_model_options.set_is_training(False)
# player1_model_options.set_save_model(False)

# Configure game
engine = PZGameEngine(env)
controller = GameController(engine)
# controller.set_player_0("model", player0_options)
controller.set_player_1("model", player1_model_options)
controller.set_game_limit(50000)
controller.set_win_threshold(0.85)
controller.set_save_history(True)
controller.set_track_scores(True)

for i in range(20):
    if i % 2 == 0:
        controller.set_player_0("better_random")
    elif i % 3 == 0:
        controller.set_player_0("model", player0_options)
    else:
        controller.set_player_0("mcts", player1_mcts_options)

    controller.start_game_loop()

    record = TrainingRecord()
    record.make_training_record(controller)
    line = record.to_string()

    with open("training_records.txt", "a") as file:
        file.write(line)

    controller.reset()

controller.game_engine.end_game()