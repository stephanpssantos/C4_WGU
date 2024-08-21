class Node:
    def __init__(self, game_engine, parent=None):
        self.game_engine = game_engine
        self.parent = parent
        self.children = []
        self.action = None
        self.visits = 0
        self.value = 0