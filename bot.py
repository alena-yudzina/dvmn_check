import logging
import os
import time
import urllib.parse

import requests
import telegram
from dotenv import load_dotenv


def form_message(lesson_info):

    lesson_title = lesson_info['lesson_title']
    message_title = 'У вас проверили работу "{}"'.format(lesson_title)

    if lesson_info['is_negative']:
        message_result = 'К сожалению, в работе нашлись ошибки.'
    else:
        message_result = 'Преподавателю все понравилось, можно приступать к следующему уроку!'

    lesson_url = lesson_info['lesson_url']
    lesson_url = urllib.parse.urljoin('https://dvmn.org/', lesson_url)
    message_url = 'Ссылка на урок {}'.format(lesson_url)

    message = '{0}\n\n{1}\n\n{2}'.format(message_title, message_result, message_url)
    return message


def main():
    load_dotenv()
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']

    bot = telegram.Bot(token=bot_token)
    logging.warning('Бот запущен')

    headers = {
        'Authorization': dvmn_token
    }
    timestamp = ''
    url = 'https://dvmn.org/api/long_polling/'

    while True:
        payload = {
            'timestamp': timestamp
            }
        try:
            response = requests.get(url, headers=headers, timeout=60, params=payload)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(60)
            continue

        answer = response.json()
        if answer['status'] == 'timeout':
            timestamp = answer['timestamp_to_request']
            continue
        lesson_info = answer['new_attempts'][0]
        timestamp = answer['last_attempt_timestamp']

        message = form_message(lesson_info)
        bot.send_message(text=message, chat_id=chat_id)


if __name__ == '__main__':
    main()
