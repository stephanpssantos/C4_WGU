class TrainingRecord:
    def __init__(self):
        self.player0 = None
        self.player1 = None
        self.winner = None
        self.win_threshold = 0
        self.games_played = 0
        self.start_time = None
        self.end_time = None
        self.saved_model_name = None
        self.player0_history = None
        self.player1_history = None

    def make_training_record(self, controller):
        self.player0 = controller.game_engine.player0.describe()
        self.player1 = controller.game_engine.player1.describe()
        self.winner = controller.game_engine.winner
        self.win_threshold = controller.win_threshold
        self.games_played = controller.game_number
        self.start_time = controller.start_time
        self.end_time = controller.end_time
        self.player0_history = controller.history0_filename
        self.player1_history = controller.history1_filename
        
        filename = next(item for item in controller.game_engine.termination_info if item is not None or "")
        self.saved_model_name = filename

    def to_string(self):
        vals = [self.player0, self.player1, self.winner, self.win_threshold, self.games_played, self.start_time, self.end_time, self.saved_model_name, self.player0_history, self.player1_history]
        vals = [str(item) for item in vals]
        return ",".join(vals) + "\n"
