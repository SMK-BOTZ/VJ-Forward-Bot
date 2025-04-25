import asyncio
from config import Config
import pyrogram
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pymongo import MongoClient

client = MongoClient(Config.DB_URL)
db = client[Config.DB_NAME]
requested_users = db.requested_users


async def ForceSub(c: Client, m: Message):
    try:
        invite_link = await c.create_chat_invite_link(
            chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        invite_link = await c.create_chat_invite_link(
            chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL))
    except Exception as err:
        print(f"Uɴᴀʙʟᴇ ᴛᴏ ᴅᴏ ғᴏʀᴄᴇ sᴜʙsᴄʀɪʙᴇ ᴛᴏ {Config.UPDATES_CHANNEL}\n\nError: {err}")
        return 200
    try:
        user = await c.get_chat_member(
            chat_id=(int(Config.UPDATES_CHANNEL) if Config.UPDATES_CHANNEL.startswith("-100") else Config.UPDATES_CHANNEL),
            user_id=m.from_user.id)
        if user.status == "kicked":
            await c.send_message(
                chat_id=m.from_user.id,
                text="Sᴏʀʀʏ sɪʀ, ʏᴏᴜ ᴀʀᴇ ʙᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
                disable_web_page_preview=True,
                parse_mode="Markdown",

            )
            return 400
    except UserNotParticipant:
        await c.send_message(
            chat_id=m.from_user.id,
            text="**Pʟᴇᴀsᴇ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ ᴍʏ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ!**\n\n**Cʟɪᴄᴋ 'ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ' ᴀɴᴅ ᴛʜᴇɴ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴀɢᴀɪɴ.**",  # Important instruction
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link),
                        InlineKeyboardButton(text="ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link),
                        InlineKeyboardButton(text="ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ",
                                             url=f"https://t.me/{Config.UPDATES_CHANNEL}?startjoin=true")
                    ],
                    [
                        InlineKeyboardButton("↻ Tʀʏ Aɢᴀɪɴ", url='https://t.me/BinarYForwarDBoT?start=start_')
                    ]
                ]
            )
        )
        return 400
    except Exception:
        await c.send_message(
            chat_id=m.from_user.id,
            text="Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ. Cᴏɴᴛᴀᴄᴛ ᴍʏ ᴀᴅᴍɪɴ.",
            disable_web_page_preview=True,
            parse_mode="Markdown",
        )
        return 400
    return 200


@Client.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    # Workaround: Assume they requested if they start the bot
    requested_users.insert_one({"user_id": user_id})
    await message.reply_text("Welcome! You've been noted as requesting to join.  If you are approved you can use the bot.")


# 5.  Middleware/Filter (Pyrogram)
@Client.on_message(filters.command(["your_bot_command_1", "your_bot_command_2", ...]))  # Add your bot's commands
async def check_request(client, message):
    user_id = message.from_user.id
    user = requested_users.find_one({"user_id": user_id})
    if not user:
        await message.reply_text("Please request to join the channel first and then start the bot!")
        return  # Stop processing the command
    else:
        # User has requested, continue with the command's logic
        await message.reply_text("Command executed!")  # Replace with your actual command logic


# 6. Admin Approval Handling (Example - Simple Command)
@Client.on_message(filters.command("approve") & filters.user(Config.ADMIN_USER_ID))  # Replace with admin user ID
async def approve_user(client, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /approve <user_id>")
        return

    try:
        user_id_to_approve = int(message.command[1])
        requested_users.update_one({"user_id": user_id_to_approve}, {"$set": {"approved": True}})
        await message.reply_text(f"User {user_id_to_approve} approved.")
    except ValueError:
        await message.reply_text("Invalid user ID.")
