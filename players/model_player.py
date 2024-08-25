import tensorflow as tf
import numpy as np
import random
import copy
from pathlib import Path
from datetime import datetime
import constants
from players.player import Player
from players.model_player_options import ModelPlayerOptions
from ml.replay_buffer import ReplayBuffer
from ml.dqn import DeepQNetwork

class ModelPlayer(Player):
    def __init__(self, name, options=None):
        self.name = name
        self.is_training = False
        self.save_model = False
        self.starting_model_path = None
        self._configure(options)

    def get_action(self, board, moves):
        q_values = np.expand_dims(board, axis=0)
        action = self._policy(q_values, moves)

        if self.is_training:
            self._update_replay_buffer(q_values, action)
        
        return action
    
    def early_termination(self):
        if not self.save_model: return ""
        filename = self._make_filename()
        self.q_net.save(filename)
        return filename.name
    
    def end_game(self, board, winner):
        if not self.is_training: return

        if winner == "draw": reward = 0
        elif winner == self.name: reward = 1
        else: reward = -1

        if (self.is_training):
            self.replay_buffer.append(
                self.prev_observation, 
                self.prev_action,
                0,
                board,
                1)
            self.replay_buffer.commit(reward)
            self.prev_action = None
            self.prev_observation = None
            self.epsilon = max(constants.E_MIN, constants.E_DECAY * self.epsilon)
            self._train()
        return
    
    def clone(self):
        # options = ModelPlayerOptions()
        # options.set_is_training = False
        # options.set_save_model = False
        # options.set_base_q_net = self.q_net
        # return ModelPlayer(self.name, options)
        return self
    
    def describe(self):
        is_training = "training" if self.is_training else "not-training"
        starting_model = "" if self.starting_model_path is None else "_" + str(self.starting_model_path.name)
        return "model_" + self.name + "_" + is_training + starting_model

    def _configure(self, options):
        if options is None:
            return
        if options.is_training:
            self.is_training = True
            self.prev_observation = None
            self.prev_action = None
            self.epsilon = constants.EPSILON
            self.optimizer = tf.keras.optimizers.Adam(learning_rate=constants.ALPHA)
            self.replay_buffer = ReplayBuffer(constants.MEMORY_SIZE, constants.MINIBATCH_SIZE)
            self.q_target_net = DeepQNetwork()
        if options.save_model:
            self.save_model = True
        if options.base_q_net is not None:
            self.q_net = options.base_q_net
        elif options.model_path is not None:
            self.starting_model_path = options.model_path
            self.q_net = tf.keras.models.load_model(options.model_path)
        else:
            self.q_net = DeepQNetwork()
        if options.model_path is not None and options.is_training:
            self.q_target_net.set_weights(self.q_net.get_weights())
        return

    def _policy(self, q_values, moves):
        # epsilon greedy policy
        if not self.is_training or random.random() > self.epsilon:
            return self._exploit(q_values, moves)
        else:
            return self._explore(moves)

    def _exploit(self, q_values, moves):
        output = []

        # compute score for each potential position
        for col in range(len(moves)):
            if moves[col] == 0:
                output.append(float('-inf'))
            elif moves[col] == 1:
                q_values_copy = copy.deepcopy(q_values)
                new_board_state = self._place_piece(q_values_copy, col)
                result = self.q_net(new_board_state)
                output.append(result[0][0])

        # return position with best score
        return np.argmax(output)
    
    def _explore(self, moves):
        # drop randomly in any open spot
        columns = [i for i, v in enumerate(moves) if v == 1]
        return random.choice(columns)
    
    def _update_replay_buffer(self, q_values, action):
        q_values_copy = copy.deepcopy(q_values)
        new_board_state = self._place_piece(q_values_copy, action)
        update_obs = np.squeeze(new_board_state, axis=0)

        if self.prev_observation is not None:
            self.replay_buffer.append(
                self.prev_observation, 
                self.prev_action,
                0,
                update_obs,
                0)
            
        self.prev_action = action
        self.prev_observation = update_obs
        return
    
    def _train(self):
        if not self.replay_buffer.check_update_conditions(): return

        experiences = self.replay_buffer.get_experiences()
        rewards, next_states = experiences[2:4]

        # doesn't work so well
        # agent_learn(experiences, self.q_net, self.q_target_net, self.optimizer)

        y_targets = rewards
        self.q_net.train_on_batch(next_states, y_targets)    
    
    def _place_piece(self, board, col):
        player = 0 if self.name == "player_0" else 1
        row = 5 # default (top row)

        # check which row to drop piece in
        for i in range(6):
            if board[0][i][col][0] == 0 and board[0][i][col][1] == 0:
                row = i

        board[0][row][col][0] = 1

        return board
    
    def _make_filename(self):
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = self.name + "_" + current_datetime + ".keras"
        abs_path = Path(__file__).parent.parent / "ml" / "saved_models" / file_name
        return abs_path