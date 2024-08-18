import tensorflow as tf
from replay_buffer import ReplayBuffer
# from strategies.no_strategy import NoStrategy
import constants

# this class will have training methods
# it'll be called by the game or game controller clas only when it's time for it to
# act, and that can be playing a move or training itself

class Player:
    def __init__(self, name, strategy, strategy_options = None):
        self.name = name
        self.strategy = strategy
        self.is_ready = False

    # def configure_agent(self):
    #     if self.strategy is None:
    #         self.strategy = NoStrategy()

    #     # if self.is_training:
    #     #     self.prev_observation = None
    #     #     self.prev_action = None
    #     #     self.epsilon = constants.EPSILON
    #     #     self.optimizer = tf.keras.optimizers.Adam(learning_rate=constants.ALPHA)
    #     #     self.replay_buffer = ReplayBuffer(constants.MEMORY_SIZE, constants.MINIBATCH_SIZE)

    #     self.is_ready = True

    # def set_name(self):
    #     pass

    # def set_is_training(self):
    #     pass

    # def set_strategy(self, strategy):
    #     pass

    # def check_state(self):
    #     if self.is_ready == False:
    #         self.configure_agent()

    def get_action(self, board_state, moves):
        # self.check_state()
        return self.strategy.get_action(board_state, moves)
        
        
