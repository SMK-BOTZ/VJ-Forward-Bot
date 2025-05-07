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
current_ui = "default"

ui_layouts = {
    "default": [[
        InlineKeyboardButton('❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ ❣️', url='https://t.me/kingvj01')
    ],[
        InlineKeyboardButton('🔍 sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ', url='https://t.me/vj_bot_disscussion'),
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/vj_botz')
    ],[
        InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='abo    ]],
    "minimal": [[
        InlineKeyboardButton('👨‍💻 Help', callback_data='help')
    ],[
        InlineKeyboardButton('❌ Close', callback_data='close')
    ]]
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
    reply_markup = InlineKeyboardMarkup(get_main_buttons())
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Script.START_TXT.format(message.from_user.first_name))

@Client.on_message(filters.private & filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client, message):
    msg = await message.reply_text(text="<i>Trying to restarting.....</i>")
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
    execle(sys.executable, sys.executable, "main.py", environ)

@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot, query):
    buttons = [[
        InlineKeyboardButton('• ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ?', callback_data='how_to_use')
    ],[
            InlineKeyboardButton('• sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
            InlineKeyboardButton('• sᴛᴀᴛᴜs ', callback_data='status')
    ],[
            InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back'),
            InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(text=Script.HELP_TXT, reply_markup=reply_markup)

@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot, query):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot, query):
    reply_markup = InlineKeyboardMarkup(main_buttons)
    await query.message.edit_text(
       reply_markup=reply_markup,
       text=Script.START_TXT.format(query.from_user.first_name))

@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot, query):
    buttons = [[
         InlineKeyboardButton('💳 ᴅᴏɴᴀᴛᴇ', callback_data='donate'),
         InlineKeyboardButton('ᴄᴏᴘʏʀɪɢʜᴛ', callback_data='copyright'),
         InlineKeyboardButton('ꜱᴛᴀᴛꜱ ✨️', callback_data='status')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot, query):
    users_count, bots_count = await db.total_users_bots_count()
    forwardings = await db.forwad_count()
    upt = await get_bot_uptime(START_TIME)
    buttons = [[
        InlineKeyboardButton('• back', callback_data='help'),
        InlineKeyboardButton('ꜱʏꜱᴛᴇᴍ ꜱᴛᴀᴛꜱ •', callback_data='systm_sts'),
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await query.message.edit_text(
        text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

@Client.on_callback_query(filters.regex(r'^donate'))
async def donate(bot, query):
    await query.message.edit_text(
        text=DONATE_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back')]])
    )

@Client.on_callback_query(filters.regex(r'^copyright'))
async def donate(bot, query):
    await query.message.edit_text(
        text=COPYRIGHT_TXT,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('• ʙᴀᴄᴋ', callback_data='back')]])
    )

@Client.on_message(filters.private & filters.command(['changeui']) & filters.user(Config.BOT_OWNER))
async def change_ui(client, message):
    global current_ui
    args = message.text.split()
    if len(args) != 2:
        await message.reply_text("Usage: /changeui <default|minimal>")
        return
    new_ui = args[1]
    if new_ui in ui_layouts:
        current_ui = new_ui
        await message.reply_text(f"✅ UI changed to: {new_ui}")
    else:
        await message.reply_text("❌ Invalid UI. Available options: " + ", ".join(ui_layouts.keys()))


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

