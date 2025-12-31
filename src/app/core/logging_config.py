import logging
import sys
from pathlib import Path

from app.core.config import settings


def setup_logging():
    log_format = "[%(asctime)s] %(levelname)s (%(name)s) %(message)s"
    formatter = logging.Formatter(log_format)

    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    clean_project_name = settings.PROJECT_NAME.replace(" ", "_").lower()
    log_file = log_dir / f"{clean_project_name}.log"

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=settings.LOG_LEVEL, handlers=[stream_handler, file_handler]
    )

    loggers_to_fix = ["uvicorn", "uvicorn.error", "uvicorn.access"]

    for logger_name in loggers_to_fix:
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = False

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        logger.setLevel(settings.LOG_LEVEL)
