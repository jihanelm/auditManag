import logging.config

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # important pour uvicorn
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 1024*1024*5,
            "backupCount": 3,
            "formatter": "default",
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["file", "console"]
    }
}

def setup_logger():
    logging.config.dictConfig(LOG_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info("Logging initialisé avec succès")
    return logger
