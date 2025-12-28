#from pathlib import Path

#CONFIG_FILE_PATH = Path("./config/config.yaml")
#PARAMS_FILE_PATH = Path("params.yaml")

from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).resolve().parents[3]

CONFIG_FILE_PATH = ROOT_DIR / "config" / "config.yaml"
PARAMS_FILE_PATH = ROOT_DIR / "params.yaml"
