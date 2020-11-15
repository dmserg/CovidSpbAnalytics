import configparser
from TelegramMessagesUtils import dump_messages, get_telegram_client

def main():
    download_covid_data('channel_messages_msk.json')

def download_covid_data(filename):
    config = configparser.ConfigParser()
    config.read("config.ini")

    client = get_telegram_client(config)
    with client:
        client.loop.run_until_complete(dump_messages(client, filename, "https://t.me/COVID2019_official"))

if __name__ == '__main__':
    main()
