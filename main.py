from textwrap import dedent
from time import sleep

from environs import Env
import requests
import telegram


def main():
    env = Env()
    env.read_env()
    devman_token = env('DEVMAN_TOKEN')
    url = env('DEVMAN_URL')
    telegram_token = env('TELEGRAM_TOKEN')
    tg_chat_id = env('TG_CHAT_ID')
    bot = telegram.Bot(token=telegram_token)
    headers = {'Authorization': f'Token {devman_token}'}
    timestamp = None
    while True:
        try:
            params = {'timestamp': timestamp}
            timestamp = ''
            response = requests.get(url, headers=headers, params=params)
            checks = response.json()
            status = checks.get('status')
            if status == 'found':
                timestamp = checks['last_attempt_timestamp']
                new_attempt = checks['new_attempts'][0]
                if new_attempt['is_negative']:
                    message = dedent(
                        f'''\
                        У вас проверили работу "{new_attempt["lesson_title"]}" 
                        К сожалению, в работе нашлись ошибки.
                        Ссылка на урок: {new_attempt["lesson_url"]}'''
                    )
                else:
                    message = dedent(
                        f'''\
                        У вас проверили работу "{new_attempt["lesson_title"]}"
                        Преподавателю все понравилось,
                        можно приступать к следующему уроку!
                        Ссылка на урок: {new_attempt["lesson_url"]}'''
                    )
                bot.send_message(chat_id=tg_chat_id, text=message)
            elif status == 'timeout':
                timestamp = checks['timestamp_to_request']
            else:
                pass
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            sleep(60)


if __name__ == '__main__':
    main()
