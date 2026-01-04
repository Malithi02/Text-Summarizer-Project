from textSummarizer.config.configuration import ConfiguartionManager
from textSummarizer.logging import logger
from textSummarizer.components.model_trainer import ModelTrainer

class ModelTrainerPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfiguartionManager()
        model_trainer_config = config.get_model_trainer_config()
        print(model_trainer_config)

        model_trainer = ModelTrainer(config=model_trainer_config)
        model_trainer.train()