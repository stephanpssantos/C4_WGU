from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def get_action(self, board, moves):
        pass

    @abstractmethod
    def end_game(self, board, winner):
        pass

    @abstractmethod
    def early_termination(self):
        pass

    @abstractmethod
    def clone(self):
        pass

    @abstractmethod
    def describe(self):
        pass