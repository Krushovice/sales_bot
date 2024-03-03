import logging
from logging.handlers import RotatingFileHandler


def setup_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )
    # Добавляем обработчик для записи в файл
    file_handler = RotatingFileHandler("app.log", maxBytes=100000, backupCount=5)
    file_handler.setFormatter(
        logging.Formatter(
            "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
        )
    )
    logger.addHandler(file_handler)

    return logger
