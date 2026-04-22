from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db
from config import PHOTO_URL

@Client.on_message(filters.command("stats"))
async def stats_command(client, message):
    msg = await message.reply("<tg-emoji emoji-id='5451646226975955576'>⌛️</tg-emoji> **Processing data...**", quote=True)
    
    def get_size(bytes, suffix="B"):
        factor = 1024
        for unit in ["", "K", "M", "G", "T", "P"]:
            if bytes < factor:
                return f"{bytes:.2f}{unit}{suffix}"
            bytes /= factor

    MAX_DB_SIZE = 536870912

    users_count = await db.users.count_documents({})
    files_count = await db.files.count_documents({})
    groups_count = await db.groups.count_documents({})
    
    try:
        db_stats = await db.users.database.command("dbstats")
        used_bytes = db_stats['storageSize']
        used_size = get_size(used_bytes)
        max_size = get_size(MAX_DB_SIZE)
        
        percentage = (used_bytes / MAX_DB_SIZE) * 100
        
        bar_len = 10
        filled_len = int(bar_len * percentage / 100)
        bar = '▓' * filled_len + '░' * (bar_len - filled_len)
        
        db_info = (
            f"🗄 <u>**Database Storage:**</u>\n"
            f"**★ Used:** `{used_size}`\n"
            f"**★ Total:** `{max_size}`\n"
            f"★ **Status:** [{bar}] `{percentage:.2f}%`"
        )
    except Exception as e:
        db_info = f"❌ Unable to retrieve technical data.\n`{e}`"

    text = (
        f"📊 <u>**Bot Statistics:**</u>\n\n"
        f"🤖 <u>**Bot Status:**</u>\n"
        f"★ **Files:** `{files_count}`\n"
        f"★ **Users:** `{users_count}`\n"
        f"★ **Groups:** `{groups_count}`\n\n"
        f"{db_info}"
    )
    
    btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("✘ Close", callback_data="closea", style=enums.ButtonStyle.DANGER)]
    ])
    
    await msg.delete()
    await message.reply_photo(
        PHOTO_URL, 
        caption=text, 
        reply_markup=btn,
        quote=True
    )
