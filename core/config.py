import os
import sys
from pathlib import Path
from typing import List
from starlette.config import Config
from starlette.datastructures import Secret, CommaSeparatedStrings


BASE_DIR = Path(__file__).parent.parent
config = Config(".env")


API_PREFIX = "/api"
VERSION = "0.0.0"
PROJECT_NAME: str = config("PROJECT_NAME", default="Campaign Management Services") 



ORIGINS: List[str] = config("ORIGINS", cast=CommaSeparatedStrings, default=[])
DEBUG: bool = config("DEBUG", cast=bool, default=True)
LOG_LEVEL: str = config("LOG_LEVEL",default="INFO")
LOG_RETENTION_DAYS:int = config("LOG_RETENTION_DAYS",default=10)
BASE_LOG_PATH: str = config("BASE_LOG_PATH",default="")

# database config
DATABASE_HOST: str = config("DATABASE_HOST", default="")
DATABSASE_NAME: str = config("DATABSASE_NAME", default="")
DATABASE_USERNAME: str = config("DATABASE_USERNAME", default="")
DATABASE_PASSWORD: str = config("DATABASE_PASSWORD", default="")
