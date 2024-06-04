# Core packages
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.client.messages import _MessagesIter
from telethon.tl.types import (
    PeerChannel,
    InputPeerChannel,
    ChatFull,
    UserFull,
    User,
)
from telethon.tl.functions.channels import GetFullChannelRequest

# Assistive packages
from pwinput import pwinput

# Parsers and Basic functions
import os
from colorama import Fore

__all__ = ["setup_image_download"]


async def download_image(messages: _MessagesIter, path: str):
    async for message in messages:
        if message.photo:
            msg = f"\033[0K{Fore.LIGHTBLUE_EX}>> Message ID: {message.id}\r"
            print(msg, end="")
            await message.download_media(file=path)


async def setup_image_download(client: TelegramClient, phone: str) -> None:
    await client.start()
    print(f"{Fore.LIGHTGREEN_EX}Connection Established...")

    if not await client.is_user_authorized():
        await client.send_code_request(phone)

        try:
            print(f"{Fore.LIGHTCYAN_EX}Verification Code? ", end="")
            await client.sign_in(phone=phone, code=input())
        except SessionPasswordNeededError:
            await client.sign_in(
                password=pwinput(prompt=f"{Fore.LIGHTBLUE_EX}Telegram Password? ")
            )
    print(f"{Fore.LIGHTCYAN_EX}Channel (ID, URL, or Name)? ", end="")
    channel: str = input()

    entity: PeerChannel | str
    if channel.isdigit():
        entity = PeerChannel(int(channel))
    else:
        entity = channel

    myChannel: InputPeerChannel = await client.get_input_entity(entity)

    channel_title: str
    if "user_id" in myChannel.stringify():
        channel_: UserFull = await client(GetFullUserRequest(myChannel.user_id))
        user_details: User = channel_.users[0]
        channel_title = " ".join([user_details.first_name, user_details.last_name])
    elif "channel_id" in myChannel.stringify():
        channel_: ChatFull = await client(GetFullChannelRequest(myChannel.channel_id))
        channel_title = channel_.chats[0].title
    else:
        channel_title = "Personal (ME)"

    # Reading messages
    messages: _MessagesIter = client.iter_messages(myChannel)
    path = os.path.join(os.getcwd(), channel_title)

    os.makedirs(path, exist_ok=True)
    print()
    await download_image(messages, path)
    await client.disconnect()
    print()


if __name__ == "__main__":
    from Telegram import create_client
    from Constants import USERNAME, API_ID, API_HASH

    client = create_client(USERNAME, API_ID, API_HASH)
    with client:
        client.loop.run_until_complete(setup_image_download(client))
