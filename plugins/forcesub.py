import asyncio
from config import Config
import pyrogram
from pyrogram import Client,filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message



async def ForceSub(c: Client, m: Message):
    
    all_channels_unsubscribed = False  # Flag to track if user is unsubscribed from any channel
    
    for channel_id in Config.FORCESUB_CHANNELS:  # Iterate through all channels
        try:
            if str(channel_id).startswith("-100"):
                chat_id = int(channel_id)
            else:
                chat_id = channel_id
            
            invite_link = await c.create_chat_invite_link(chat_id=chat_id)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            invite_link = await c.create_chat_invite_link(chat_id=chat_id)
        except Exception as err:
            print(f"Uɴᴀʙʟᴇ ᴛᴏ ᴅᴏ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴛᴏ {channel_id}\n\nError: {err}")
            continue  # Skip to the next channel

        try:
            user = await c.get_chat_member(chat_id=chat_id, user_id=m.from_user.id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=m.from_user.id,
                    text="Sᴏʀʀʏ sɪʀ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ @Sahil_x_official .",
                    disable_web_page_preview=True,
                    parse_mode="Markdown",
                )
                return 400  # Exit if user is banned from any channel
        except UserNotParticipant:
            all_channels_unsubscribed = True  # Set flag to True if user is not a participant
            await c.send_message(
                chat_id=m.from_user.id,
                text="**Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ!**\n\n Oɴʟʏ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link)
                        ],[
                            InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", url='https://t.me/Mikasa_Forward_Bot?start=start_')
                        ]
                    ]
                )
            )
            return 400  # Exit if user is not a participant
        except Exception:
            await c.send_message(
                chat_id=m.from_user.id,
                text="Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
                disable_web_page_preview=True,
                parse_mode="Markdown",
            )
            return 400  # Exit on error
    
    if all_channels_unsubscribed:
        return 400  # Return 400 if user is unsubscribed from any channel
    
    return 200
