import base64
import os
import random
import string

from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import Message

from bot import LOGGER
from bot.config import SUDO_USERID


async def isAdmin(message: Message) -> bool:
    """
    Return True if the message is from owner or admin of the group or sudo of the bot.
    """

    if not message.from_user:
        return
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return

    user_id = message.from_user.id
    if user_id in SUDO_USERID:
        return True

    check_status = await message.chat.get_member(user_id)
    return check_status.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]


def get_readable_time(seconds: int) -> str:
    """
    Return a human-readable time format
    """

    result = ""
    (days, remainder) = divmod(seconds, 86400)
    days = int(days)

    if days != 0:
        result += f"{days}d "
    (hours, remainder) = divmod(remainder, 3600)
    hours = int(hours)

    if hours != 0:
        result += f"{hours}h "
    (minutes, seconds) = divmod(remainder, 60)
    minutes = int(minutes)

    if minutes != 0:
        result += f"{minutes}m "

    seconds = int(seconds)
    result += f"{seconds}s "
    return result


def get_readable_bytes(size: str) -> str:
    """
    Return a human readable file size from bytes.
    """

    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}

    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0

    while size > power:
        size /= power
        raised_to_pow += 1

    return f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"


def random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))


def saveImg(self, bs64: str) -> str:
    try:
        with open(f"images/{random_string(7)}.jpg", "wb") as f:
            f.write(base64.b64decode(bs64))
            f.close()
        return os.path.abspath(f.name)
    except Exception as e:
        LOGGER(__name__).error(e)
