import logging
from enum import Enum
from pathlib import Path

from app.core.config import logger_settings

Path(logger_settings.LOGGER_FILE_PATH).parent.mkdir(exist_ok=True)


class Handlers(Enum):
    console = "console"
    app_file = "app_file"


HANDLERS = [
    handler
    for handler in logger_settings.HANDLERS.split(",")
    if handler in Handlers.__members__.keys()
]
LOG_LEVEL = logging._nameToLevel.get(logger_settings.LOG_LEVEL.upper(), "INFO")


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app_formatter": {
            "()": "logging.Formatter",
            "datefmt": "%Y.%m.%d %H:%M:%S",
            "fmt": "[%(asctime)s.%(msecs)03d] %(levelname)s | %(name)s:%(funcName)s.%(lineno)d - %(message)s",  # noqa
        },
        "app_middleware_formatter": {
            "()": "logging.Formatter",
            "datefmt": "%Y.%m.%d %H:%M:%S",
            "fmt": "[%(asctime)s.%(msecs)03d] %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        Handlers.console.value: {
            "formatter": "app_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        Handlers.app_file.value: {
            "formatter": "app_formatter",
            "class": "logging.FileHandler",
            "filename": logger_settings.LOGGER_FILE_PATH,
        },
        Handlers.console.value
        + "_middleware": {
            "formatter": "app_middleware_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        Handlers.app_file.value
        + "_middleware": {
            "formatter": "app_middleware_formatter",
            "class": "logging.FileHandler",
            "filename": logger_settings.LOGGER_FILE_PATH,
        },
    },
    "loggers": {
        "app": {
            "handlers": HANDLERS,
            "level": LOG_LEVEL,
        },
        "app.core.middleware": {
            "handlers": [h + "_middleware" for h in HANDLERS],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}
