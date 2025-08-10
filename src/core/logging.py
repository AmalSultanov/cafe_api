import logging
import sys
from pathlib import Path

from src.core.config import get_settings

settings = get_settings()


def setup_logging():
    logs_dir = Path("src/logs")
    logs_dir.mkdir(exist_ok=True)
    
    log_level = logging.DEBUG if settings.fastapi_debug else logging.INFO
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler('src/logs/app.log')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def get_logger(name: str = "app") -> logging.Logger:
    return logging.getLogger(name)


logger = get_logger("cafe_api")


def log(message: str, level: str = "info"):
    log_func = getattr(logger, level.lower(), logger.info)
    log_func(message)
