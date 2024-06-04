from packages import (
    setup_messages,
    create_client,
    clean,
    setup_image_download,
    DateTimeEncoder,
    USERNAME,
    PHONE,
    API_ID,
    API_HASH,
)

# Types
from telethon import TelegramClient
from telethon.tl.types import Message

# Utility
from colorama import init
import json

init(autoreset=True)


def read_message_callback(
    client: TelegramClient, channel_title: str, messages: list[Message]
):
    temp: list[dict] = []
    for message in messages:
        temp.append(message.to_dict())
    output_file = "telegram_%s.json" % channel_title.lower().replace(" ", "_")
    with open(output_file, "w") as file:
        json.dump(
            sorted(temp, key=lambda x: x["id"]), file, cls=DateTimeEncoder, indent=4
        )


if __name__ == "__main__":
    import sys

    if not len(sys.argv) > 1:
        choice = "message"
    else:
        choice = sys.argv[1].lower()

        if choice == "help":
            print(f"Choices: Image/Message")
            sys.exit(0)

    client = create_client(USERNAME, API_ID, API_HASH)
    with client:
        if choice == "message":
            client.loop.run_until_complete(
                setup_messages(
                    client,
                    phone=PHONE,
                    limit=10,
                    offset_id=0,
                    callback=read_message_callback,
                )
            )
        elif choice == "image":
            client.loop.run_until_complete(setup_image_download(client, phone=PHONE))
    # clean() # Removes session files
