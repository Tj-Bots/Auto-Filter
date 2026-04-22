import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command(["json", "js"]))
async def jsonify(_, message):
    close_btn = InlineKeyboardMarkup([[InlineKeyboardButton("✘ Close", callback_data="closea")]])
    target_message = message.reply_to_message if message.reply_to_message else message

    try:
        await message.reply_text(f"```json\n{target_message}```", reply_markup=close_btn, quote=True)
    except Exception as e:
        try:
            with open("json.txt", "w", encoding="utf-8") as f:
                f.write(str(target_message))
            
            await message.reply_document(
                document="json.txt",
                caption=f"❌ **Error:** Message is too long.\nSent as a file instead.",
                reply_markup=close_btn,
                quote=True
            )
            os.remove("json.txt")
        except Exception as error:
            await message.reply(f"Critical error: {error}")

@Client.on_message(filters.command("written"))
async def create_file(c, message):
    if not message.reply_to_message:
        return await message.reply("❌ **Error:** You must reply to a message with text.", quote=True)

    content = message.reply_to_message.text or message.reply_to_message.caption
    
    if not content:
        return await message.reply("❌ No text found in the message you replied to.", quote=True)

    if len(message.command) < 2:
        file_name = "Text.txt"
    else:
        user_filename = message.text.split(None, 1)[1]
        
        if "." not in user_filename:
            file_name = f"{user_filename}.txt"
        else:
            file_name = user_filename
    
    try:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        
        await message.reply_document(
            document=file_name,
            caption=f"",
            quote=True
        )
        os.remove(file_name)
    except Exception as e:
        await message.reply(f"❌ Error creating file:\n`{e}`")
