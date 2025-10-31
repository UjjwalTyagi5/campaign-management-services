import os
import sys
from loguru import logger
from core.config import DEBUG,LOG_LEVEL,LOG_RETENTION_DAYS,BASE_LOG_PATH

def setup_logger():
    """
    Configure the Loguru logger for the application.

    - Sets log level based on DEBUG or LOG_LEVEL from config.
    - Creates the log directory if it doesn't exist.
    - Logs to a file (rotated daily, retained for LOG_RETENTION_DAYS).
    - Also logs to stderr for console output.
    - Handles directory creation errors gracefully.
    """
    if DEBUG:
        level = 'DEBUG'
    else:
        level = LOG_LEVEL

    log_dir = os.path.join(BASE_LOG_PATH,"app")
    try:
        os.makedirs(log_dir,exist_ok=True)
        assert os.access(log_dir,os.W_OK), f"Cannot write to {log_dir}"
    except Exception as e:
        print(f"Failed to create or write the log dir {log_dir} : {e}")
    log_path = os.path.join(log_dir,"app_{time:YYYY-MM-DD}.log")
    logger.remove()
    logger.add(log_path,
               rotation="1 day",
               retention=f"{LOG_RETENTION_DAYS} days",
               level=level)
    logger.add(sys.stderr, level=level)


