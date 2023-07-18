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
            api_response = response.json()
            status = api_response.get('status')
            if status == 'found':
                new_attempt = api_response['new_attempts'][0]
                if new_attempt['is_negative']:
                    message = (
                        f'У вас проверили работу "{new_attempt["lesson_title"]}"'
                        '\nК сожалению, в работе нашлись ошибки.'
                        f'\nСсылка на урок: {new_attempt["lesson_url"]}'
                    )
                else:
                    message = (
                        f'У вас проверили работу "{new_attempt["lesson_title"]}"'
                        '\nПреподавателю все понравилось,'
                        'можно приступать к следующему уроку!'
                        f'\nСсылка на урок: {new_attempt["lesson_url"]}'
                    )
                bot.send_message(chat_id=tg_chat_id, text=message)
            elif status == 'timeout':
                timestamp = api_response['timestamp_to_request']
                print('timeout')
            else:
                print('unexpected status')
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass


if __name__ == '__main__':
    main()
