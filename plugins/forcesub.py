import asyncio
from config import Config  # Assuming Config is where you store channel IDs
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from typing import List, Union

async def ForceSub(c: Client, m: Message) -> int:
    """
    Force users to subscribe to multiple channels before using the bot.

    Args:
        c (Client): The Pyrogram Client instance.
        m (Message): The Pyrogram Message object.

    Returns:
        int: 200 if the user is subscribed to all channels, 400 otherwise.
    """

    if not Config.UPDATES_CHANNEL:
        return 200  # No force_sub channel specified

    channels: List[Union[str, int]] = Config.UPDATES_CHANNEL  # Can be a single channel or list

    if not isinstance(channels, list):
        channels = [channels]  # Ensure it's a list

    user_id = m.from_user.id

    for channel_id in channels:
        channel_id = int(channel_id) if isinstance(channel_id, str) and channel_id.startswith("-100") else channel_id
        try:
            try:
                invite_link = await c.create_chat_invite_link(chat_id=channel_id)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                invite_link = await c.create_chat_invite_link(chat_id=channel_id)
            except Exception as err:
                print(f"Uɴᴀʙʟᴇ ᴛᴏ ᴅᴏ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴛᴏ {channel_id}\n\nError: {err}")
                return 200 # If one channel fails, don't block the user. Might need revision

            user = await c.get_chat_member(chat_id=channel_id, user_id=user_id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=user_id,
                    text="Sᴏʀʀʏ sɪʀ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ ɪɴ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
                    disable_web_page_preview=True,
                    parse_mode="Markdown",
                )
                return 400
        except UserNotParticipant:
            await c.send_message(
                chat_id=user_id,
                text="**Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ!**\n\n Oɴʟʏ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link)
                        ],[
                            InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", url=f'https://t.me/{c.me.username}?start=start_')
                        ]
                    ]
                )
            )
            return 400
        except Exception as e:
            print(f"Error checking channel {channel_id}: {e}")
            await c.send_message(
                chat_id=user_id,
                text="Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
                disable_web_page_preview=True,
                parse_mode="Markdown",
            )
            return 400

    return 200
