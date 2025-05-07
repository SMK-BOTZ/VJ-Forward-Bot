from plugins.forcesub import *
import os
import sys
import asyncio 
from database import Db, db
from config import Config, temp
from script import Script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument
import psutil
import time as time
from os import environ, execle, system

START_TIME = time.time()

# Define the DONATE_TXT variable in this script
DONATE_TXT = """ if you liked me ❤️. consider make a donation to support my developer 👦

UPI ID - <code>coming soon...</code>
"""

# Define the COPYRIGHT_TXT variable in this script
COPYRIGHT_TXT = """ ᴀʟʟ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴄʀᴇᴅɪᴛꜱ
ʙᴀꜱᴇ ʀᴇᴘᴏ = ᴜɴᴋɴᴏᴡɴ ꜱᴏᴜʀᴄᴇ
ꜰᴏʀᴄᴇꜱᴜʙ = @Anmol0700
ʀᴇᴘᴏ ᴇʀʀᴏʀꜱ ꜰɪxᴇᴅ = @Sahil_x_official
ᴍᴜʟᴛɪᴘʟᴇ ꜰᴏʀᴄᴇꜱᴜʙ = @Necromancer_sl
ɴᴇᴡ ᴄᴀʟʟʙᴀᴄᴋꜱ ᴀɴᴅ ᴇʀʀᴏʀꜱ ꜰɪxᴇᴅ = @Miss_Siya_1
ɪꜰ ɪ ꜰᴏʀɢᴏᴛ ᴀɴʏᴏɴᴇ ɪɴ ᴛʜɪꜱ ᴛʜᴇɴ ᴛʜᴀᴛꜱ ʏᴏᴜʀ ᴘʀᴏʙʟᴇᴍ ɴᴏᴛ ᴍɪɴᴇ.
"""

# Place this at the top, where `main_buttons` is defined
# Your existing ui_layouts and current_ui definitions
# ui_layouts = { ... }
# current_ui = "default"

def get_ui(section_key: str):
    """
    Retrieves the InlineKeyboardMarkup for a given section of the current UI.
    """
    # Get the dictionary of sections for the current_ui,
    # defaulting to the "default" UI if current_ui is not found.
    current_layout_sections = ui_layouts.get(current_ui, ui_layouts.get("kokan", {}))
    
    # Get the specific button layout for the requested section_key.
    buttons = current_layout_sections.get(section_key)
    
    if buttons:
        return InlineKeyboardMarkup(buttons)
    else:
        # Fallback or error handling if the section_key is not found for the UI
        # For example, return None or an empty markup
        # This depends on how you want to handle missing UI sections
        print(f"Warning: UI section '{section_key}' not found for UI '{current_ui}'.")
        return None # Or return InlineKeyboardMarkup([])
        
current_ui = "kokan"

ui_layouts = {
    "kokan": {
        "start": [[
            InlineKeyboardButton('❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ ❣️', url='https://t.me/Shubham_X_Official')
        ],[
            InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ', url='https://t.me/Arise_Botz'),
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇꜱ', url='https://t.me/Arise_Bots')
        ],[
            InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')
        ],[
            InlineKeyboardButton('⚙ ꜱᴇᴛᴛɪɴɢꜱ', callback_data='settings#main')
        ]],
        "about": [[
            InlineKeyboardButton('💳 ᴅᴏɴᴀᴛᴇ', callback_data='donate'),
            InlineKeyboardButton('ᴄᴏᴘʏʀɪɢʜᴛ', callback_data='copyright'),
            InlineKeyboardButton('ꜱᴛᴀᴛꜱ ✨️', callback_data='status')
        ]],
        "status": [[
            InlineKeyboardButton('🔙 back', callback_data='help'),
            InlineKeyboardButton('ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ 📊', callback_data='systm_sts')
        ]],
        "help": [[
        InlineKeyboardButton('❗️ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ⁉️', callback_data='how_to_use')
        ],[
            InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('sᴛᴀᴛᴜs 📊', callback_data='status')
        ],[
            InlineKeyboardButton('🔙 ʙᴀᴄᴋ', callback_data='back'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ 🗯', callback_data='about')
        ]],
        "how_to_use": [[
            InlineKeyboardButton('⚙️ sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('Back 👉🏻', callback_data='start')
        ]],
        "donate": [[
            InlineKeyboardButton('🧑‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back', callback_data='start')
        ]],
        "copyright": [[
            InlineKeyboardButton('🧑‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back 👉🏻', callback_data='start')
        ]],
    },

    "Yareyare": {
        "start": [[
        InlineKeyboardButton('❗️ ʜᴇʟᴘ', callback_data='help')
        ],[
        InlineKeyboardButton('📜 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/Arise_Bots'),
        InlineKeyboardButton('📣 ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/Arise_Botss')
        ],[
        InlineKeyboardButton('💳 ᴅᴏɴᴀᴛᴇ', callback_data='donate')
        ]],
        "how_to_use": [[
            InlineKeyboardButton('• sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('Back •', callback_data='start')
        ]],
        "status": [[
            InlineKeyboardButton('• back', callback_data='help'),
            InlineKeyboardButton('ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ •', callback_data='systm_sts')
        ]],
        "help": [[
        InlineKeyboardButton('• ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ?', callback_data='how_to_use')
        ],[
            InlineKeyboardButton('• sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('sᴛᴀᴛᴜs •', callback_data='status')
        ],[
            InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ •', callback_data='about')
        ]],
        "donate": [[
            InlineKeyboardButton('• ᴅᴇᴠᴇʟᴏᴘᴇʀ', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back •', callback_data='start')
        ]],
        "copyright": [[
            InlineKeyboardButton('• ᴅᴇᴠᴇʟᴏᴘᴇʀ ', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back •', callback_data='start')
        ]],
        "about": [[
            InlineKeyboardButton('🪡 ᴅᴇᴠᴇʟᴏᴘᴇʀ 🪡', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back •', callback_data='start')
        ]]
    },

    "Okiru": {
        "start": [[
        InlineKeyboardButton('🦋 ᴜᴘᴅᴀᴛᴇs ', url='https://t.me/JISSHU_BOTS'),
        InlineKeyboardButton(' sᴜᴘᴘᴏʀᴛ ✨', url='https://t.me/Jisshu_support')
        ],[
        InlineKeyboardButton('🛠️ ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton(' ᴀʙᴏᴜᴛ 😎', callback_data='about')
        ],[
        InlineKeyboardButton('🛠️ sᴇᴛᴛɪɴɢs ⚙️', callback_data='settings#main')
        ]],
        "how_to_use": [[
            InlineKeyboardButton('⛔ Back', callback_data='help'),
        ]],
        "status": [[
            InlineKeyboardButton('• back', callback_data='help'),
            InlineKeyboardButton('ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ •', callback_data='systm_sts')
        ]],
        "help": [[
            InlineKeyboardButton('🛠️ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ 🛠️', callback_data='how_to_use')
            ],[
            InlineKeyboardButton('⚙️ sᴇᴛᴛɪɴɢs ⚙️', callback_data='settings#main'),
            InlineKeyboardButton('📊 sᴛᴀᴛᴜs 📊', callback_data='status')
            ],[
            InlineKeyboardButton('⛔ ʙᴀᴄᴋ', callback_data='back')
            ]],
        "donate": [[
            InlineKeyboardButton('🦋 ᴄᴏᴘʏʀɪɢʜᴛ', callback_data='copyright'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ ✨', callback_data='about')
        ]],
        "copyright": [[
            InlineKeyboardButton('🦋 ᴅᴏɴᴀᴛᴇ', callback_data='donate'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ ✨', callback_data='about')
        ]],
        "about": [[
            InlineKeyboardButton('🦋 ᴄᴏᴘʏʀɪɢʜᴛ', callback_data='copyright'),
            InlineKeyboardButton('ᴅᴏɴᴀᴛᴇ ✨', callback_data='donate')
        ]]
    },

    "sungspecial": {
        "start": [[
            InlineKeyboardButton('⎝⎝✧ᴅᴇᴠᴇʟᴏᴘᴇʀ✧⎠⎠', url='https://t.me/Shubham_X_Official')
        ],[
            InlineKeyboardButton('⎝⎝✧ᵃ𝖛є𝙣𝗲𝒈𝗲𝒓✧⎠⎠ sᴜᴘᴘᴏʀᴛ', url='https://t.me/Arise_Botz'),
            InlineKeyboardButton('⎝⎝✧ᴜᴘᴅᴀᴛᴇꜱ✧⎠⎠', url='https://t.me/Arise_Bots')
        ],[
            InlineKeyboardButton('⎝⎝✧ʜᴇʟᴘ✧⎠⎠ ', callback_data='help'),
            InlineKeyboardButton('⎝⎝✧ᴀʙᴏᴜᴛ✧⎠⎠', callback_data='about')
        ],[
            InlineKeyboardButton('⎝⎝✧ꜱᴇᴛᴛɪɴɢꜱ✧⎠⎠', callback_data='settings#main')
        ]],
        "about": [[
            InlineKeyboardButton('⎝⎝✧ᴅᴏɴᴀᴛᴇ✧⎠⎠', callback_data='donate'),
            InlineKeyboardButton('⎝⎝✧ᴄᴏᴘʏʀɪɢʜᴛ✧⎠⎠', callback_data='copyright'),
            InlineKeyboardButton('⎝⎝✧ꜱᴛᴀᴛꜱ✧⎠⎠', callback_data='status')
        ]],
        "status": [[
            InlineKeyboardButton('⎝⎝✧back✧⎠⎠', callback_data='help'),
            InlineKeyboardButton('⎝⎝✧ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ✧⎠⎠', callback_data='systm_sts')
        ]],
        "help": [[
        InlineKeyboardButton('⎝⎝✧ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ✧⎠⎠', callback_data='how_to_use')
        ],[
            InlineKeyboardButton('⎝⎝✧sᴇᴛᴛɪɴɢs✧⎠⎠', callback_data='settings#main'),
            InlineKeyboardButton('⎝⎝✧sᴛᴀᴛᴜs✧⎠⎠', callback_data='status')
        ],[
            InlineKeyboardButton('⎝⎝✧ʙᴀᴄᴋ✧⎠⎠', callback_data='back'),
            InlineKeyboardButton('⎝⎝✧ᴀʙᴏᴜᴛ✧⎠⎠', callback_data='about')
        ]],
        "how_to_use": [[
            InlineKeyboardButton('⎝⎝✧sᴇᴛᴛɪɴɢs✧⎠⎠', callback_data='settings#main'),
            InlineKeyboardButton('⎝⎝✧Back✧⎠⎠', callback_data='start')
        ]],
        "donate": [[
            InlineKeyboardButton('⎝⎝✧ᴅᴇᴠᴇʟᴏᴘᴇʀ✧⎠⎠', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('⎝⎝✧Back✧⎠⎠', callback_data='start')
        ]],
        "copyright": [[
            InlineKeyboardButton('⎝⎝✧ᴅᴇᴠᴇʟᴏᴘᴇʀ✧⎠⎠', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('⎝⎝✧Back✧⎠⎠Back', callback_data='start')
        ]],
    },

    "yomaivo": {
        "start": [[
            InlineKeyboardButton('❣️ 開発者 ❣️', url='https://t.me/Shubham_X_Official')
        ],[
            InlineKeyboardButton('🔍 サポート', url='https://t.me/Arise_Botz'),
            InlineKeyboardButton('🤖 アップデート', url='https://t.me/Arise_Bots')
        ],[
            InlineKeyboardButton('👨‍💻 ヘルプ', callback_data='help'),
            InlineKeyboardButton('💁 について', callback_data='about')
        ],[
            InlineKeyboardButton('⚙ 設定', callback_data='settings#main')
        ]],
        "about": [[
            InlineKeyboardButton('💳 寄付する', callback_data='donate'),
            InlineKeyboardButton('著作権', callback_data='copyright'),
            InlineKeyboardButton('統計 ✨️', callback_data='status')
        ]],
        "status": [[
            InlineKeyboardButton('🔙 戻る', callback_data='help'),
            InlineKeyboardButton('システム統計 📊', callback_data='systm_sts')
        ]],
        "help": [[
        InlineKeyboardButton('❗️ 使い方 ⁉️', callback_data='how_to_use')
        ],[
            InlineKeyboardButton('⚙ 設定', callback_data='settings#main'),
            InlineKeyboardButton('状態 📊', callback_data='status')
        ],[
            InlineKeyboardButton('🔙 戻る', callback_data='back'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ 🗯', callback_data='about')
        ]],
        "how_to_use": [[
            InlineKeyboardButton('⚙️ 設定', callback_data='settings#main'),
            InlineKeyboardButton('戻る 👉🏻', callback_data='start')
        ]],
        "donate": [[
            InlineKeyboardButton('🧑‍💻 開発者 🧑‍💻', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('戻る', callback_data='start')
        ]],
        "copyright": [[
            InlineKeyboardButton('🧑‍💻 開発者 🧑‍💻', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('戻る 👉🏻', callback_data='start')
        ]],
    },
    
    "arisebots": {
        "start": [[
            InlineKeyboardButton('❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ ❣️', url='https://t.me/Shubham_X_Official')
        ],[
            InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ', url='https://t.me/Arise_Botz'),
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇꜱ', url='https://t.me/Arise_Bots')
        ],[
            InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
            InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')
        ],[
            InlineKeyboardButton('⚙ ꜱᴇᴛᴛɪɴɢꜱ', callback_data='settings#main')
        ]],
        "about": [[
            InlineKeyboardButton('💳 ᴅᴏɴᴀᴛᴇ', callback_data='donate'),
            InlineKeyboardButton('ᴄᴏᴘʏʀɪɢʜᴛ', callback_data='copyright'),
            InlineKeyboardButton('ꜱᴛᴀᴛꜱ ✨️', callback_data='status')
        ]],
        "status": [[
            InlineKeyboardButton('🔙 back', callback_data='help'),
            InlineKeyboardButton('ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ 📊', callback_data='systm_sts')
        ]],
        "help": [[
        InlineKeyboardButton('❗️ ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ⁉️', callback_data='how_to_use')
        ],[
            InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('sᴛᴀᴛᴜs 📊', callback_data='status')
        ],[
            InlineKeyboardButton('🔙 ʙᴀᴄᴋ', callback_data='back'),
            InlineKeyboardButton('ᴀʙᴏᴜᴛ 🗯', callback_data='about')
        ]],
        "how_to_use": [[
            InlineKeyboardButton('⚙️ sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('Back 👉🏻', callback_data='start')
        ]],
        "donate": [[
            InlineKeyboardButton('🧑‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back', callback_data='start')
        ]],
        "copyright": [[
            InlineKeyboardButton('🧑‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 🧑‍💻', url='https://t.me/Shubham_X_Official'),
            InlineKeyboardButton('Back 👉🏻', callback_data='start')
        ]],
    }
    
}


def get_main_buttons():
    return ui_layouts.get(current_ui, ui_layouts["default"])


@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    user = message.from_user

    # Check for force subscription
    Fsub = await ForceSub(client, message)
    if Fsub == 400:
        return
    
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id, user.first_name)
    await client.send_message(
        chat_id=message.chat.id,
        text=Script.START_TXT.format(user.first_name),
        reply_markup=get_ui("start")
    )

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text(text="<i>Trying to restarting.....</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    reply_markup = get_ui("help") # Use the new "help" section
    await query.message.edit_text(
        text=Script.HELP_TXT,
        reply_markup=reply_markup

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Script.START_TXT.format(query.from_user.first_name))

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=get_ui("about"),
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    upt = await get_bot_uptime(START_TIME)
    await query.message.edit_text(
        text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=get_ui("status"),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex(r'^copyright'))
async def donate(bot, query):
    await query.message.edit_text(
        text=COPYRIGHT_TXT,
        reply_markup=get_ui("copyright")
    )

@Client.on_callback_query(filters.regex(r'^donate'))
async def donate(bot, query):
    await query.message.edit_text(
        text=DONATE_TXT,
        reply_markup=get_ui("donate")
    )

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    # The original 'buttons' and 'reply_markup' are no longer needed
    # buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    # reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=get_ui("how_to_use"),
        disable_web_page_preview=True
    )

@Client.on_message(filters.private & filters.command(['changeui']) & filters.user(Config.BOT_OWNER))
async def change_ui(client, message):
    global current_ui
    args = message.text.split()
    if len(args) != 2:
        await message.reply_text("Usage: /changeui <default|minimal>")
        return
    ui = args[1]
    if ui not in ui_layouts:
        await message.reply_text(f"Invalid UI. Available: {', '.join(ui_layouts.keys())}")
        return
    current_ui = ui
    await message.reply_text(f"✅ UI changed to {ui}. All future messages will reflect the new layout.")


@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024**3)  # Convert to GB
    used_space = disk_usage.used / (1024**3)    # Convert to GB
    free_space = disk_usage.free / (1024**3)
    text = f"""
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ</b>: <code>{total_space:.2f} GB</code>
║┣⪼ <b>ᴜsᴇᴅ</b>: <code>{used_space:.2f} GB</code>
║┣⪼ <b>ꜰʀᴇᴇ</b>: <code>{free_space:.2f} GB</code>
║┣⪼ <b>ᴄᴘᴜ</b>: <code>{cpu}%</code>
║┣⪼ <b>ʀᴀᴍ</b>: <code>{ram}%</code>
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text,
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

async def get_bot_uptime(start_time):
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_hours != 0:
        uptime_string += f" {uptime_hours % 24}H"
    if uptime_minutes != 0:
        uptime_string += f" {uptime_minutes % 60}M"
    uptime_string += f" {uptime_seconds % 60} Sec"
    return uptime_string   

