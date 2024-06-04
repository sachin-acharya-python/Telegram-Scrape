from typing import Any
from datetime import datetime
import configparser
import json

__all__ = ["config", "DateTimeEncoder", "API_ID", "API_HASH", "PHONE", "USERNAME"]


# JSON date parser
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, bytes):
            return list(o)
        return json.JSONEncoder.default(self, o)


config = configparser.ConfigParser()
config.read("config.ini")

API_ID: str = config["Telegram"]["api_id"]
API_HASH: str = config["Telegram"]["api_hash"]

PHONE: str = config["Telegram"]["phone"]
USERNAME: str = config["Telegram"]["username"]
