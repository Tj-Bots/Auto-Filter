import uuid
from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery, 
    InlineQueryResultCachedVideo, 
    InlineQueryResultCachedDocument,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton, 
    InlineKeyboardMarkup
)
from database import db
from config import PHOTO_URL

@Client.on_inline_query()
async def inline_search(client: Client, query: InlineQuery):
    results = []
    string = query.query.strip()
    
    if not string:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="🔍 Search Movies and Series",
                description="Type a movie or series name to search",
                input_message_content=InputTextMessageContent(
                    "**To use inline search, simply click the button and type the movie/series name you want.**"
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔎 Click here to search", switch_inline_query_current_chat="")]
                ]),
                thumb_url=PHOTO_URL
            )
        )
        await query.answer(results, cache_time=0)
        return

    files = await db.search_files(string)
    
    if not files:
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title="No results found",
                description=f"No files found for: {string}",
                input_message_content=InputTextMessageContent(f"**No results found for: {string}**"),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔎 Try another search", switch_inline_query_current_chat="")]
                ]),
                thumb_url="https://cdn-icons-png.flaticon.com/512/2748/2748614.png"
            )
        )
    else:
        for file in files[:50]:
            f_name = file['file_name']
            file_id = file['file_id']
            file_type = file.get('file_type', 'document')
            
            f_size = file.get('file_size', 0)
            if f_size > 1024 * 1024 * 1024:
                size_text = f"{f_size / (1024 * 1024 * 1024):.2f} GB"
            else:
                size_text = f"{f_size / (1024 * 1024):.2f} MB"

            caption = f"**{f_name}**\n💾 **Size:** {size_text}"
            reply_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔎 Search again", switch_inline_query_current_chat=string)]
            ])

            if file_type == 'video':
                results.append(
                    InlineQueryResultCachedVideo(
                        id=str(uuid.uuid4()),
                        video_file_id=file_id,
                        title=f"🎬 {f_name}",
                        description=f"💾 Size: {size_text}",
                        caption=caption,
                        reply_markup=reply_markup
                    )
                )
            else:
                results.append(
                    InlineQueryResultCachedDocument(
                        id=str(uuid.uuid4()),
                        document_file_id=file_id,
                        title=f"📁 {f_name}",
                        description=f"💾 Size: {size_text}",
                        caption=caption,
                        reply_markup=reply_markup
                    )
                )

    await query.answer(results, cache_time=1)
