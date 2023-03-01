import logging
from logging import config

log_config = {
    "version": 1,
    "root": {"handlers": ["console"], "level": "DEBUG"},
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG",
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        }
    },
}

config.dictConfig(log_config)

logger = logging.getLogger("portfolio")
