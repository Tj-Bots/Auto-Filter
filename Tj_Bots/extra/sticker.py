from pyrogram import Client, filters

@Client.on_message(filters.command("stickerid"))
async def stickerid(bot, message):
    if message.reply_to_message and message.reply_to_message.sticker:
        sticker = message.reply_to_message.sticker
        await message.reply_text(
            f"**Sticker ID:**\n`{sticker.file_id}`\n\n**Unique ID:**\n`{sticker.file_unique_id}`",
            quote=True
        )
    else:
        await message.reply_text("❌ Please reply to a sticker with this command.", quote=True)
