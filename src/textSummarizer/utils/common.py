import os
import box.exceptions as BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from box import configBox   
from pathlib import Path
from typing import Any

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> configBox:
    """Reads a yaml file and returns

    Args:
        path_to_yaml (Path): Path like input

    Raises:
        ValueError: if yaml file is empty
        e: empty file    

    Returns:
        configBox: configBox type
    """
    try:
        with open(path_to_yaml, 'r') as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return configBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")  
    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories: list,verbose=True):
    """Create list of directories

    Args:
        path_to_directories (list): list of path like directories
        ignore_log (bool, optional): ignore log messages. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:

           logger.info(f"created directory at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """Get size in KB

    Args:
        path (Path): Path like input

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path)/1024)
    return f"~ {size_in_kb} KB"