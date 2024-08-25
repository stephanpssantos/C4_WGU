import copy
from engine.game_engine import GameEngine

class SimGameEngine(GameEngine):
    def __init__(self, board, next_player):
        super().__init__()
        self.board = board
        self.next_player = next_player
        self.winner = None

    def start_game(self):
        while self.winner is None:
            player = self.player1 if self.next_player else self.player0
            player_num = self.next_player
            self.next_player = int(not self.next_player)
            action = player.get_action(self.get_board(), self.get_moves())
            row = self._place_piece(player_num, action)
            game_won = self._check_winner(row, action, player_num)
            if game_won: self.winner = player
            game_draw = self._check_draw()
            if game_draw: self.winner = "draw"
        return self.winner

    def reset(self):
        self.next_player = 0
        self.winner = None

    def get_moves(self):
        moves = []
        for i in range(len(self.board[0])):
            if self.board[0][i][0] == 0 and self.board[0][i][1] == 0:
                moves.append(1)
            else:
                moves.append(0)
        return moves
    
    def get_board(self):
        return self.board
    
    def game_over(self):
        return self.winner is not None
    
    def early_termination(self):
        return
    
    def end_game(self):
        return
    
    def play_one_move(self, action):
        if self.winner is not None: raise Exception("play_one_move called when game already over")
        player_num = self.next_player
        self._invert_board()
        self.next_player = int(not self.next_player)
        row = self._place_piece(player_num, action)
        game_won = self._check_winner(row, action, player_num)
        if game_won: self.winner = self.player1 if player_num else self.player0
        game_draw = self._check_draw()
        if game_draw: self.winner = "draw"  
        return self.winner
    
    def clone(self):
        board_copy = copy.deepcopy(self.board)
        engine = SimGameEngine(board_copy, self.next_player)
        engine.winner = self.winner
        engine.player0 = self.player0.clone()
        engine.player1 = self.player1.clone()
        return engine
    
    def _place_piece(self, player, position):
        row = 0
        for i in range(len(self.board)):
            if self.board[i][position][0] == 0 \
            and self.board[i][position][1] == 0:
                row = i
        self.board[row][position][player] = 1
        return row
    
    def _check_draw(self):
        moves = self.get_moves()
        if all(x == 0 for x in moves): return True
        else: return False

    def _check_winner(self, move_row, move_col, player):
        def go_direction(row, col, direction, count):
            if direction in (1, 2, 3):
                row -= 1
            if direction in (5, 6, 7):
                row += 1
            if direction in (3, 4, 5):
                col -= 1
            if direction in (1, 7, 8):
                col += 1

            next_position = self.board[row][col] \
                if row in range(len(self.board)) \
                and col in range(len(self.board[0])) else None

            if next_position is None: return count
            elif next_position[int(player)] == 0: return count
            else: return go_direction(row, col, direction, count + 1)

        nw_se = 1 + go_direction(move_row, move_col, 1, 0) + go_direction(move_row, move_col, 5, 0)
        w_e = 1 + go_direction(move_row, move_col, 2, 0) + go_direction(move_row, move_col, 6, 0)
        sw_ne = 1 + go_direction(move_row, move_col, 3, 0) + go_direction(move_row, move_col, 7, 0)
        n_s = 1 + go_direction(move_row, move_col, 4, 0) + go_direction(move_row, move_col, 8, 0)

        most = max(nw_se, w_e, sw_ne, n_s)
        return most >= 4
    
    def _invert_board(self):
        if self.next_player == 0: return
        board_copy = copy.deepcopy(self.board)
        self.board = board_copy[:,:,::-1]