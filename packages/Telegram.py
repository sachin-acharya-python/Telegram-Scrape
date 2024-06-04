from telethon import TelegramClient
from sqlite3 import OperationalError

__all__ = ['create_client']

# Creating Client Object
def create_client(username: str, api_id: str, api_hash: str) -> TelegramClient:
    try:
        return TelegramClient(username, api_id=api_id, api_hash=api_hash)
    except OperationalError:
        return TelegramClient(None, api_id=api_id, api_hash=api_hash)
