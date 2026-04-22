import os
from pyrogram import Client, filters

@Client.on_message(filters.command("extract_thumbnail"))
async def extract_thumbnail_handler(client, message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to a video or file that has a thumbnail.", quote=True)
    
    reply = message.reply_to_message
    media = reply.video or reply.document or reply.animation or reply.audio
    
    if not media or not hasattr(media, "thumbs") or not media.thumbs:
        return await message.reply_text("❌ No thumbnail found in this media.", quote=True)

    status = await message.reply_text("⏳ **Extracting thumbnail...**", quote=True)
    
    try:
      
        thumb = media.thumbs[-1]
        file_path = await client.download_media(thumb.file_id)
        
        if file_path:
            await message.reply_photo(
                photo=file_path,
                quote=True
            )
            await status.delete()
            
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            await status.edit("❌ Failed to download the thumbnail.")
            
    except Exception as e:
        await status.edit(f"❌ Extraction error: `{e}`")
