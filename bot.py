import os

import requests
import telegram
import urllib.parse
from dotenv import load_dotenv


def form_message(response_dict):

    lesson_title = response_dict['new_attempts'][0]['lesson_title']
    message_title = 'У вас проверили работу "{}"'.format(lesson_title)

    if response_dict['new_attempts'][0]['is_negative']:
        message_result = 'К сожалению, в работе нашлись ошибки.'
    else:
        message_result = 'Преподавателю все понравилось, можно приступать к следующему уроку!'
    
    lesson_url = response_dict['new_attempts'][0]['lesson_url']
    lesson_url = urllib.parse.urljoin('https://dvmn.org/', lesson_url)
    message_url = 'Ссылка на урок {}'.format(lesson_url)

    message = message_title + '\n' + '\n' + message_result + '\n' + '\n' + message_url
    return message


def main():
    load_dotenv()
    bot_token = os.environ['BOT_TOKEN']
    chat_id = os.environ['CHAT_ID']
    dvmn_token = os.environ['DVMN_TOKEN']

    bot = telegram.Bot(token=bot_token)

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
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            continue
        timestamp =  response.json()['new_attempts'][0]['timestamp']
        message = form_message(response.json())
        bot.send_message(text=message, chat_id=chat_id)


if __name__ == '__main__':
    main()
