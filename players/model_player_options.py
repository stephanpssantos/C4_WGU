from pathlib import Path

class ModelPlayerOptions:
    def __init__(self):
        self.is_training = True
        self.save_model = True
        self.model_path = None

    def set_model_path(self, value):
        file_path = Path(__file__).parent.parent / "ml" / "saved_models" / value
        self.model_path = file_path