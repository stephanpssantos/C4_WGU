from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def get_action(self, board, moves):
        pass

    @abstractmethod
    def end_game(self, board, winner):
        pass