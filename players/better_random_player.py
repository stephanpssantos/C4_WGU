import random
import numpy as np
from players.player import Player

class BetterRandomPlayer(Player):
    def __init__(self, name):
        self.name = name

    def get_action(self, board, moves):
        columns = [i for i, v in enumerate(moves) if v == 1]
        player = 0 if self.name == "player_0" else 1

        # this will prioritize wins over blocking enemy wins
        opponent_winner = -1
        for i in columns:
            row = self._place_piece(board, i)
            winner = self._check_winner(board, row, i, player)
            if winner == 1: return i
            if winner == -1: opponent_winner = i

        return opponent_winner if opponent_winner >= 0 else random.choice(columns)
    
    def early_termination(self):
        return ""
    
    def end_game(self, board, winner):
        return
    
    def clone(self):
        return BetterRandomPlayer(self.name)
    
    def describe(self):
        return "random_" + self.name
    
    def _check_winner(self, board, move_row, move_col, player):
        def go_direction(row, col, direction, count):
            if direction in (1, 2, 3):
                row -= 1
            if direction in (5, 6, 7):
                row += 1
            if direction in (3, 4, 5):
                col -= 1
            if direction in (1, 7, 8):
                col += 1

            next_position = board[row][col] \
                if row in range(len(board)) \
                and col in range(len(board[0])) else None

            if next_position is None: return count
            elif next_position[0] == 0 and next_position[1] == 0: 
                return count
            else:
                if count[0] >= count[1] and next_position[0] == 1: count[0] += 1
                if count[1] >= count[0] and next_position[1] == 1: count[1] += 1
                return go_direction(row, col, direction, count)

        nw_se = np.add(go_direction(move_row, move_col, 1, [0, 0]), go_direction(move_row, move_col, 5, [0, 0]))
        w_e = np.add(go_direction(move_row, move_col, 2, [0, 0]), go_direction(move_row, move_col, 6, [0, 0]))
        sw_ne = np.add(go_direction(move_row, move_col, 3, [0, 0]), go_direction(move_row, move_col, 7, [0, 0]))
        n_s = np.add(go_direction(move_row, move_col, 4, [0, 0]), go_direction(move_row, move_col, 8, [0, 0]))

        player_num = int(player)
        opponent_num = int(not player)
        player_score = max(nw_se[player_num], w_e[player_num], sw_ne[player_num], n_s[player_num])
        opponent_score = max(nw_se[opponent_num], w_e[opponent_num], sw_ne[opponent_num], n_s[opponent_num])

        if player_score >= 3: return 1
        elif opponent_score >= 3: return -1
        else: return 0
    
    def _place_piece(self, board, position):
        row = 0
        for i in range(len(board)):
            if board[i][position][0] == 0 \
            and board[i][position][1] == 0:
                row = i
        return row