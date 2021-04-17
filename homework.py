import logging
import os
import time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_TOKEN = os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

API_URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'

# create and configure a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
_formatter = logging.Formatter(
    '%(asctime)s - [%(levelname)s] - %(name)s - %(message)s'
)
_file_name = Path(__file__).stem
_handler = RotatingFileHandler(
    f'{_file_name}.log',
    maxBytes=50000000,
    backupCount=5,
    encoding="UTF-8",
)
_handler.setFormatter(_formatter)
logger.addHandler(_handler)


def parse_homework_status(homework):
    '''Check the status and generate an appropriate message.'''
    homework_name = homework['homework_name']
    if homework['status'] == 'reviewing':
        verdict = 'Но не до конца.'
    elif homework['status'] == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = (
            'Ревьюеру всё понравилось, '
            'можно приступать к следующему уроку.'
        )
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    '''Check for status updates from a specified time.'''
    homework_statuses = requests.get(
        API_URL,
        headers={
            'Authorization': f'OAuth {PRAKTIKUM_TOKEN}',
        },
        params={
            'from_date': current_timestamp,
        },
    )
    return homework_statuses.json()


def send_message(message, bot_client):
    '''Sending the generated message to the user.'''
    logger.info(f'bot send: {message}')
    return bot_client.send_message(
        CHAT_ID,
        message,
    )


def main():
    '''Launch bot;
    at a certain interval to request the status of homework;
    if there are status updates, send a message to the user.'''
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    logger.debug('bot started working')
    current_timestamp = int(time.time())

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(
                    parse_homework_status(
                        new_homework.get('homeworks')[0]
                    ),
                    bot,
                )
            current_timestamp = new_homework.get(
                'current_date',
                current_timestamp,
            )
            time.sleep(1000)

        except Exception as e:
            print(f'Бот столкнулся с ошибкой: {e}')
            logger.error('something went wrong')
            time.sleep(5)


if __name__ == '__main__':
    main()
