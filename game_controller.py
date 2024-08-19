import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import constants
from players.player_factory import PlayerFactory

class GameController:
    def __init__(self, game_engine):
        self.game_engine = game_engine
        self.game_number = 0
        self.player0_games = []
        self.player1_games = []
        pass

    def set_players(self, player0, player1):
        self.game_engine.player0 = PlayerFactory(0, player0)
        self.game_engine.player1 = PlayerFactory(1, player1)
        return
    
    def set_game_limit(self, limit):
        self.game_limit = limit
    
    def start_game_loop(self):
        self._startup_check()
        
        while (self.game_number < self.game_limit):
            self._start_new_game()

        self.game_engine.end_game()
        pass

    def _start_new_game(self):
        if self.game_number >= self.game_limit: 
            return
        
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
        if winner == "draw":
            self.player0_games.append(0)
            self.player1_games.append(0)
        elif winner == self.game_engine.player0.name:
            self.player0_games.append(1)
            self.player1_games.append(-1)
        elif winner == self.game_engine.player1.name:
            self.player0_games.append(-1)
            self.player1_games.append(1)

        return
    
    def _console_print_results(self):
        games_counted = constants.GAME_COUNT_AVERAGE

        av_latest_points_0 = np.mean(self.player0_games[-games_counted:])
        av_latest_points_1 = np.mean(self.player1_games[-games_counted:])

        player0_wins = self.player0_games[-games_counted:].count(1)
        player1_wins = self.player1_games[-games_counted:].count(1)

        print(f"\rGame {self.game_number} | Total point average of the last {games_counted} games -  p0:{av_latest_points_0:.2f}, p1:{av_latest_points_1:.2f} | ({player0_wins} - {player1_wins})", end="")

    def plot_history(self, point_history, **kwargs):
        lower_limit = 0
        upper_limit = len(point_history)

        window_size = (upper_limit * 10) // 100

        plot_rolling_mean_only = False
        plot_data_only = False

        if kwargs:
            if "window_size" in kwargs:
                window_size = kwargs["window_size"]

            if "lower_limit" in kwargs:
                lower_limit = kwargs["lower_limit"]

            if "upper_limit" in kwargs:
                upper_limit = kwargs["upper_limit"]

            if "plot_rolling_mean_only" in kwargs:
                plot_rolling_mean_only = kwargs["plot_rolling_mean_only"]

            if "plot_data_only" in kwargs:
                plot_data_only = kwargs["plot_data_only"]

        points = point_history[lower_limit:upper_limit]

        # Generate x-axis for plotting.
        episode_num = [x for x in range(lower_limit, upper_limit)]

        # Use Pandas to calculate the rolling mean (moving average).
        rolling_mean = pd.DataFrame(points).rolling(window_size).mean()

        plt.figure(figsize=(10, 7), facecolor="white")

        if plot_data_only:
            plt.plot(episode_num, points, linewidth=1, color="cyan")
        elif plot_rolling_mean_only:
            plt.plot(episode_num, rolling_mean, linewidth=2, color="magenta")
        else:
            plt.plot(episode_num, points, linewidth=1, color="cyan")
            plt.plot(episode_num, rolling_mean, linewidth=2, color="magenta")

        text_color = "black"

        ax = plt.gca()
        ax.set_facecolor("black")
        plt.grid()
        plt.xlabel("Episode", color=text_color, fontsize=30)
        plt.ylabel("Total Points", color=text_color, fontsize=30)
        yNumFmt = mticker.StrMethodFormatter("{x:,}")
        ax.yaxis.set_major_formatter(yNumFmt)
        ax.tick_params(axis="x", colors=text_color)
        ax.tick_params(axis="y", colors=text_color)
        plt.show()
