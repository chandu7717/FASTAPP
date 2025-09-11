import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logger():
    logger_type = logging.getLogger("fastapi_app")  # Creates a named logger (fastapi_app).
    logger_type.setLevel(logging.INFO)

    # Avoid adding multiple handlers when uvicorn reloads
    if not logger_type.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        # Sends logs to the console (stdout).Useful during development so you see logs in your terminal.
        console_handler.setLevel(logging.INFO)
        LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "app.log") #Getting the current file

        # File handler
        file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=1_000, backupCount=3)
        # The RotatingFileHandler = in this the logs are inserted into the app.log with size of 1MB after the file is full it will create the app.log.1 till 3 fiels
        # A special handler that writes logs to a file and automatically rotates (creates new log files) when the file size limit is reached.

        file_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

        # Logging formate current time  , levelname=ERROR,WARNING,loggername=fast_app , message = log message
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers
        logger_type.addHandler(console_handler)
        logger_type.addHandler(file_handler)

    return logger_type


logger = setup_logger()
