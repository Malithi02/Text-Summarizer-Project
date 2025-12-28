import os
from textSummarizer.logging import logger
from textSummarizer.entity import DataValidationConfig
from pathlib import Path
import os

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exists(self) -> bool:
        try:
            all_files = os.listdir(
                os.path.join("artifacts", "data_ingestion", "samsum_dataset")
            )

            validation_status = all(
                file in self.config.ALL_REQUIRED_FILES for file in all_files
            )

            # ✅ CREATE DIRECTORY IF NOT EXISTS
            status_file_path = Path(self.config.STATUS_FILE)
            status_file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(status_file_path, 'w') as f:
                f.write(f"validation status: {validation_status}\n")

            return validation_status

        except Exception as e:
            raise e
