from pathlib import Path

class ModelPlayerOptions:
    def __init__(self):
        self.is_training = True
        self.save_model = True
        self.model_path = None
        self.base_q_net = None

    def set_is_training(self, value):
        self.is_training = value

    def set_save_model(self, value):
        self.save_model = value

    def set_model_path(self, value):
        self.base_q_net = None
        file_path = Path(__file__).parent.parent / "ml" / "saved_models" / value
        self.model_path = file_path

    def set_base_q_net(self, value):
        self.model_path = None
        self.base_q_net = value