from abc import ABC, abstractmethod

class GameEngine(ABC):
    def __init__(self):
        self._player0 = None
        self._player1 = None
        self._next_player = 0

    @property
    def player0(self):
        return self._player0
    
    @player0.setter
    def player0(self, value):
        self._player0 = value

    @property
    def player1(self):
        return self._player1
    
    @player1.setter
    def player1(self, value):
        self._player1 = value

    @property
    def next_player(self):
        return self._next_player
    
    @next_player.setter
    def next_player(self, value):
        self._next_player = value

    @abstractmethod
    def start_game(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_board(self):
        pass

    @abstractmethod
    def get_moves(self):
        pass
    
    @abstractmethod
    def game_over(self):
        pass

    @abstractmethod
    def end_game(self):
        pass