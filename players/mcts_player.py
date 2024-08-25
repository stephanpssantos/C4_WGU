import math
import random
import copy
from players.mcts_node import Node
from players.player import Player
from players.random_player import RandomPlayer
from players.better_random_player import BetterRandomPlayer
from players.model_player import ModelPlayer
from players.model_player_options import ModelPlayerOptions
from players.mcts_player_options import MCTSPlayerOptions
from engine.sim_game_engine import SimGameEngine

class MCTSPlayer(Player):
    def __init__(self, name, options):
        self.name = name
        self.num_simulations = options.num_simulations
        self.clone_level = options.clone_level
        self.exploration_coeff = options.exploration_coeff
        self.player_num = 0 if name == "player_0" else 1
        # Implement the below if you want to have MCTS play against different player types
        # or if you want this to play a certain way after the first move
        # self.post_action_player = options.post_action_player

    def get_action(self, board, moves):
        sim = self._create_sim(board)
        root = Node(sim) # game_engine, parent=None

        for _ in range(self.num_simulations):
            node = root

            # Selection
            # Starting from root, select optimal child nodes until a leaf node is reached
            while node.children:
                node = self._select(node)

            # Expansion
            # If node is not a leaf (if the game isn't over), create more leaves then choose one
            if node.children:
                node = random.choice([child for child in node.children if child.visits == 0])
            elif node.game_engine.winner is None:
                node = self._expand(node)
            
            # Simulation
            # Play out the rest of the game
            reward = self._simulate(node)

            # Backpropagation
            # Update the current move with the outcome
            self._backpropagate(node, reward)

        return max(root.children, key=lambda c: c.value).action
        # return max(root.children, key=lambda c: c.visits).action
        # return self._select(root).action
    
    def early_termination(self):
        return ""
    
    def end_game(self, board, winner):
        return
    
    def clone(self):
        # unless you're implementing MCTS v different player types
        raise Exception("Don't clone MCTS player")
        # player_options = MCTSPlayerOptions(1)
        # if self.clone_level < 2:
        #     clone_level = self.clone_level + 1
        #     num_simulations = self.num_simulations // 2
        #     if num_simulations == 0: num_simulations = 1
        #     player_options = MCTSPlayerOptions(num_simulations, clone_level)
        #     return MCTSPlayer(self.name, player_options)
        # else:
        #     return RandomPlayer(self.name)
        # return RandomPlayer(self.name)
    
    def describe(self):
        return "mcts_" + self.name + "_" + str(self.num_simulations)

    def _create_sim(self, board):
        board_copy = copy.deepcopy(board)
        engine = SimGameEngine(board_copy, self.player_num)
        engine.player0 = RandomPlayer("player_0")
        engine.player1 = RandomPlayer("player_1")

        # if planning on implementing MCTS against itself or against a model,
        # here you could make it check which player it is then make it clone itself
        # below is a test, but it's too expensive
        # player_options = ModelPlayerOptions()
        # player_options.set_model_path("player_0_20240823_100953.keras")
        # player_options.set_is_training(False)
        # player_options.set_save_model(False)
        # engine.player0 = ModelPlayer("player_0", player_options)
        # engine.player1 = ModelPlayer("player_1", player_options)

        # player_options = MCTSPlayerOptions(20, 1)
        # engine.player0 = MCTSPlayer("player_0", player_options)
        # engine.player1 = MCTSPlayer("player_1", player_options)
        
        return engine

    def _select(self, node):
        def best(child):
            if child.visits == 0: return math.inf
            return child.value / child.visits + self.exploration_coeff * math.sqrt(math.log(node.visits) / child.visits)

        return max(node.children, key=best)
    
    def _expand(self, node):
        legal_moves = node.game_engine.get_moves()
        for action, valid in enumerate(legal_moves):
            if valid == 0: continue
            new_sim = node.game_engine.clone()
            new_sim.play_one_move(action)
            child = Node(new_sim, parent=node)
            child.action = action
            node.children.append(child)
        return random.choice(node.children)
    
    def _simulate(self, node):
        node.game_engine.start_game()
        winner = node.game_engine.winner
        if winner == "draw": reward = 0
        elif winner.name == self.name: reward = 1
        else: reward = -1
        return reward
    
    def _backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.value += reward
            node = node.parent