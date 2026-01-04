from textSummarizer.config.configuration import ConfiguartionManager
from textSummarizer.logging import logger
from textSummarizer.components.model_evaluation import ModelEvaluation
#from textSummarizer.config.configuration import ConfigurationManager



class ModelEvaluationPipeline:
    def __init__(self):
        pass

    def main(self):
        config = ConfiguartionManager()
        model_evaluation_config = config.get_model_evaluation_config()

        logger.info("Model Evaluation config loaded")

        model_evaluation = ModelEvaluation(config=model_evaluation_config)
        model_evaluation.evaluate()
