from environs import Env
import telegram


def main():
    env = Env()
    env.read_env()
    telegram_token = env('TELEGRAM_TOKEN')

    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id='275826730', text="I'm sorry Dave I'm afraid I can't do that.")


if __name__ == '__main__':
    main()
