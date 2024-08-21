import numpy as np
from datetime import datetime
from pathlib import Path
import constants
from players.player_factory import PlayerFactory

class GameController:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_number = 0
        self.win_threshold = 0
        self.terminate_on_threshold = False
        self.save_game_history = False
        self.track_scores = False
        self.player0_games = []
        self.player1_games = []
        self.player0_winrate = 0
        self.player1_winrate = 0
        self.history0_filename = None
        self.history1_filename = None
        self.start_time = None
        self.end_time = None

    def set_player_0(self, player0, player0_options=None):
        self.game_engine.player0 = PlayerFactory(0, player0, player0_options)

    def set_player_1(self, player1, player1_options=None):
        self.game_engine.player1 = PlayerFactory(1, player1, player1_options)
    
    def set_game_limit(self, limit):
        self.game_limit = limit

    def set_win_threshold(self, threshold, enabled=True):
        self.win_threshold = threshold
        self.terminate_on_threshold = enabled

    def set_save_history(self, value):
        self.save_game_history = value

    def set_track_scores(self, value):
        self.track_scores = value
        if not value: 
            print("Warning: score tracking disabled. Game history and win threshold also disabled.")
            self.save_game_history = False
            self.terminate_on_threshold = False
    
    def start_game_loop(self):
        self.start_time = datetime.now()
        self._startup_check()
        
        while (self.game_number < self.game_limit):
            self._start_new_game()

            if self._check_threshold():
                self.game_engine.early_termination()
                break

        self._save_game_history()
        self.game_engine.end_game()
        self.end_time = datetime.now()

    def _start_new_game(self):
        if self.game_number >= self.game_limit: return
        self.game_number += 1
        self.game_engine.reset()
        winner = self.game_engine.start_game()
        self._update_scores(winner)
        self._console_print_results()
        return

    def _startup_check(self):
        if self.game_limit is None:
            self.game_limit = 1
        if self.game_engine.player0 is None:
            self.game_engine.player0 = PlayerFactory(0, "random")
        if self.game_engine.player1 is None:
            self.game_engine.player1 = PlayerFactory(1, "random")

    def _update_scores(self, winner):
        if not self.track_scores: return

        if winner == "draw":
            self.player0_games.append(0)
            self.player1_games.append(0)
        elif winner == self.game_engine.player0.name:
            self.player0_games.append(1)
            self.player1_games.append(-1)
        elif winner == self.game_engine.player1.name:
            self.player0_games.append(-1)
            self.player1_games.append(1)

        games_counted = constants.GAME_COUNT_AVERAGE
        self.player0_winrate = np.mean(self.player0_games[-games_counted:])
        self.player1_winrate = np.mean(self.player1_games[-games_counted:])
        return
    
    def _check_threshold(self):
        if not self.terminate_on_threshold: 
            return False
        if (self.player0_winrate >= self.win_threshold or self.player1_winrate >= self.win_threshold) \
            and self.game_number >= constants.GAME_COUNT_AVERAGE:
            return True
    
    def _console_print_results(self):
        if not self.track_scores: return
        games_counted = constants.GAME_COUNT_AVERAGE
        player0_wins = self.player0_games[-games_counted:].count(1)
        player1_wins = self.player1_games[-games_counted:].count(1)

        print(f"\rGame {self.game_number} | Total point average of the last {games_counted} games -  p0:{self.player0_winrate:.2f}, p1:{self.player1_winrate:.2f} | ({player0_wins} - {player1_wins})", end="")

    def _save_game_history(self):
        if not self.save_game_history: return
        fn0 = self._make_filename("player0")
        fn1 = self._make_filename("player1")
        np.savetxt(fn0, self.player0_games, fmt="%d")
        np.savetxt(fn1, self.player1_games, fmt="%d")
        self.history0_filename = str(fn0.name)
        self.history1_filename = str(fn1.name)

    def _make_filename(self, player):
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = player + "_" + current_datetime + ".txt"
        abs_path = Path(__file__).parent / "ml" / "game_history" / file_name
        return abs_path