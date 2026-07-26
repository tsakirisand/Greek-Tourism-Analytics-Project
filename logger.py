"""
Centralized logging configuration for the Greek Tourism Project.
"""

import logging
import sys
from pathlib import Path


def setup_logger(name: str = "greek_tourism") -> logging.Logger:
    """Configures and returns a logger instance with dual output handlers.

    Logs to both standard output (console) and a file named app.log.

    Args:
        name: Name of the logger, defaults to 'greek_tourism'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid duplicate handlers if logger is already configured
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    log_file_path = Path("app.log")
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()
