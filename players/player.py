from abc import ABC, abstractmethod

class Player(ABC):
    @abstractmethod
    def get_action(self, board, moves):
        pass