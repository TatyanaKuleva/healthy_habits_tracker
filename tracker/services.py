import logging
from datetime import datetime

import requests

from config import settings

logger = logging.getLogger(__name__)


def parse_habit_time(time_str):
    """
    Парсит время из строки, поддерживая форматы HH:MM и HH:MM:SS.
    Возвращает объект time или None в случае ошибки.
    """
    if not time_str:
        return None

    # Пробуем разные форматы
    formats = ["%H:%M:%S", "%H:%M"]

    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt).time()
        except (ValueError, TypeError):
            continue

    return None


def send_telegram_message(chat_id, message):
    params = {
        "text": message,
        "chat_id": chat_id,
    }
    url = f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage"

    logger.info(f"Отправка запроса в Telegram API: url={url}, chat_id={chat_id}")

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        logger.info(
            f"Успешный ответ от Telegram API: status_code={response.status_code}, response={response.json()}"
        )
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"✗ Ошибка при отправке сообщения в Telegram: {e}", exc_info=True)
        raise
