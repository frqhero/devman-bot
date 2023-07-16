from environs import Env
import requests
import telegram


def main():
    env = Env()
    env.read_env()
    devman_token = env('DEVMAN_TOKEN')
    url = env('DEVMAN_URL')
    telegram_token = env('TELEGRAM_TOKEN')
    chat_id = env('CHAT_ID')
    bot = telegram.Bot(token=telegram_token)
    headers = {'Authorization': f'Token {devman_token}'}
    timestamp = ''
    while True:
        try:
            if not timestamp:
                response = requests.get(url, headers=headers)
            else:
                params = {'timestamp': timestamp}
                timestamp = ''
                response = requests.get(url, headers=headers, params=params)
            response = response.json()
            status = response.get('status')
            if status == 'found':
                print(response['new_attempts'])
                bot.send_message(
                    chat_id=chat_id, text='Преподаватель проверил работу!'
                )
            elif status == 'timeout':
                timestamp = response['timestamp_to_request']
                print('timeout')
            else:
                print('unexpected status')
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass


if __name__ == '__main__':
    main()
