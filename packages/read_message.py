# Core packages
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types.messages import ChannelMessages
from telethon.tl.types import (
    PeerChannel,
    InputPeerChannel,
    ChatFull,
    UserFull,
    User,
    Message,
)
from telethon.tl.functions.channels import GetFullChannelRequest

# Assistive packages
from pwinput import pwinput
from datetime import datetime

# Parsers and Basic functions
import os
from colorama import Fore
from typing import Callable

__all__ = ["setup_messages"]


def print_message(channel: str, offset_id: int, total_messages: int) -> None:
    print(
        f"""{Fore.LIGHTGREEN_EX}Message Information
    [Channel]           {channel}
    [Offset ID]         {offset_id}
    [Total Messages]    {total_messages}
    """
    )


async def read_message(
    client: TelegramClient,
    peer: InputPeerChannel,
    offset_id: int = 0,
    offset_date: datetime | None = None,
    add_offset: int = 0,
    limit: int = 100,
    max_id: int = 0,
    min_id: int = 0,
    hash: int = 0,
) -> list[Message]:
    history: ChannelMessages = await client(
        GetHistoryRequest(
            peer=peer,
            offset_id=offset_id,
            offset_date=offset_date,
            add_offset=add_offset,
            limit=limit,
            max_id=max_id,
            min_id=min_id,
            hash=hash,
        )
    )

    return history.messages


async def setup_messages(
    client: TelegramClient,
    phone: str,
    download_path: str | None = None,
    offset_id: int = 0,
    limit: int = 100,
    callback: Callable[[TelegramClient, str, list[Message]], None] | None = None,
):
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

    # Reading Messages
    total_messages: int = 0
    messages: list[Message] = []
    while True:
        print_message(channel_title, offset_id, total_messages)
        history = await read_message(
            client, myChannel, limit=limit, offset_id=offset_id
        )
        if not history:
            break

        for message in history:
            media = message.media
            if media and message.media.photo:
                if download_path:
                    filename = (
                        media.photo.file_name
                        if hasattr(media.photo, "file_name")
                        else str(media.photo.id)
                    )
                    path = os.path.join(os.getcwd(), download_path, filename)
                    await client.download_media(message, file=path)
            messages.append(message)
        offset_id = messages[-1].id
        total_messages = len(messages)

        if limit and total_messages >= limit:
            break

    if callback:
        callback(client, channel_title, messages)
    await client.disconnect()
