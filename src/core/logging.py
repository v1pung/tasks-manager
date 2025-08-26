import logging
import logging.config
import os


def setup_logging():
    """Настройка конфигурации логирования."""
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "INFO",
                "formatter": "standard",
                "filename": "logs/src.log",
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "src": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
        },
    }

    # Создаем директорию logs, если она не существует
    os.makedirs("logs", exist_ok=True)
    logging.config.dictConfig(log_config)
