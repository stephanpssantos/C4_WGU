from pettingzoo.classic import connect_four_v3
import constants
from pz_game_engine import PZGameEngine
from game_controller import GameController

# Configure environment
env = connect_four_v3.env(render_mode="human")  #  ansi or human
env.reset(seed=constants.SEED)

# Configure game
engine = PZGameEngine(env)
controller = GameController(engine)
controller.set_players("random", "random")
controller.set_game_limit(10)
controller.start_game_loop()