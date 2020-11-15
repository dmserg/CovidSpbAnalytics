from telethon.sync import TelegramClient
import json
# класс для работы с сообщениями
from telethon.tl.functions.messages import GetHistoryRequest
from datetime import date, datetime

def get_telegram_client(config):
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']
    username = config['Telegram']['username']
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    return client

async def __dump_all_messages(client, channel, filename):
    """Записывает json-файл с информацией о всех сообщениях канала/чата"""
    offset_msg = 0  # номер записи, с которой начинается считывание
    limit_msg = 100  # максимальное число записей, передаваемых за один раз

    all_messages = []  # список всех сообщений
    total_count_limit = 0  # поменяйте это значение, если вам нужны не все сообщения

    class DateTimeEncoder(json.JSONEncoder):
        '''Класс для сериализации записи дат в JSON'''

        def default(self, o):
            if isinstance(o, datetime):
                return o.isoformat()
            if isinstance(o, bytes):
                return list(o)
            return json.JSONEncoder.default(self, o)

    while True:
        history = await client(GetHistoryRequest(
            peer=channel,
            offset_id=offset_msg,
            offset_date=None, add_offset=0,
            limit=limit_msg, max_id=0, min_id=0,
            hash=0))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_msg = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open(filename, 'w', encoding='utf8') as outfile:
        json.dump(all_messages, outfile, ensure_ascii=False, cls=DateTimeEncoder)

async def dump_messages(client, filename, url):
    #url = "https://t.me/koronavirusspb"
    channel = await client.get_entity(url)
    await __dump_all_messages(client, channel, filename)