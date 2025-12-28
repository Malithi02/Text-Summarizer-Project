import os
import urllib.request as request
import zipfile
from textSummarizer.utils.common import get_size
from textSummarizer.logging import logger

from textSummarizer.entity import DataIngestionConfig
from pathlib import Path
from urllib import request

from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size, create_directories



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
        create_directories([self.config.root_dir])

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} downloaded! with following info: \n{headers}")
        else:
            logger.info(
                f"File already exists of size: "
                f"{get_size(Path(self.config.local_data_file))}"
            )

    def extract_zip_file(self):
        unzip_path = self.config.unzipped_dir
        os.makedirs(unzip_path, exist_ok=True)

        with zipfile.ZipFile(self.config.local_data_file, "r") as zip_ref:
            zip_ref.extractall(unzip_path)
