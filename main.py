from environs import Env


def main():
    env = Env()
    env.read_env()
    devman_token = env('DEVMAN_TOKEN')


if __name__ == '__main__':
    main()
