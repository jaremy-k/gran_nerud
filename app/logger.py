import logging
from datetime import datetime
import pytz
from pythonjsonlogger import json
from app.config import settings


class CustomJsonFormatter(json.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)

        # Устанавливаем московское время
        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = datetime.now(moscow_tz)

        # Форматируем timestamp
        log_record['timestamp'] = moscow_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        # Уровень логирования в верхнем регистре
        log_record['level'] = record.levelname.upper()

        # Добавляем дополнительные поля из record.args
        if hasattr(record, 'props'):
            log_record.update(record.props)


def setup_logging():
    """Настройка логгера с JSON-форматированием"""
    logger = logging.getLogger('app')
    logger.setLevel(settings.LOG_LEVEL)

    # Очистка предыдущих обработчиков
    logger.handlers.clear()

    # Создание обработчика
    handler = logging.StreamHandler()

    # Настройка форматтера
    formatter = CustomJsonFormatter(
        '%(timestamp)s %(level)s %(message)s %(module)s %(funcName)s'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = setup_logging()


# Удобная функция для структурированного логирования
def log_event(level: str, message: str, **kwargs):
    extra = {'props': kwargs}
    logger.log(getattr(logging, level.upper()), message, extra=extra)
