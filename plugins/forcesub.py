import asyncio
from config import Config
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

async def ForceSub(c: Client, m: Message):
    user_id = m.from_user.id
    channels = Config.UPDATES_CHANNELS  # Changed to UPDATES_CHANNELS
    
    must_join = []
    
    for channel in channels:
        channel_id = int(channel) if isinstance(channel, str) and channel.startswith("-100") else channel
        try:
            #  We don't create invite links in this version, as we're checking multiple channels
            user = await c.get_chat_member(chat_id=channel_id, user_id=user_id)
            if user.status == "kicked":
                await c.send_message(
                    chat_id=user_id,
                    text="Sᴏʀʀʏ sɪʀ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ @Sahil_x_official .",
                    disable_web_page_preview=True,
                    parse_mode="Markdown",
                )
                return 400
        except UserNotParticipant:
            must_join.append(channel)  # Collect channels the user hasn't joined
        except Exception as e:
            print(f"Error checking channel {channel}: {e}")
            return 500  # Or handle the error as you see fit

    if must_join:
        buttons = [[InlineKeyboardButton(text=f"Join {  (await c.get_chat(chat_id= channel )).title  if isinstance(channel, int) else channel  }", url= (await c.create_chat_invite_link(chat_id= (int(channel) if isinstance(channel, str) and channel.startswith("-100") else channel )  )).invite_link  )] for channel in must_join]
        buttons.append([InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", callback_data="check_sub")])  # Add a "Try Again" button

        await c.send_message(
            chat_id=user_id,
            text="**Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ:**\n\n Oɴʟʏ ᴄʜᴀɴɴᴇʟ sᴜʙsᴄʀɪʙᴇʀs ᴄᴀɴ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ!",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return 400

    return 200

@Client.on_callback_query(filters.regex("check_sub"))
async def check_sub(bot:Client,query):
    if await ForceSub(bot,query.message) == 200:
        await query.answer("You Have Joined All Channels")
        await query.message.delete()
    else:
        await query.answer("Please Join The Channels First!")
