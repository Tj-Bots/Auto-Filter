from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMINS
from database import db
import asyncio
import time

# Global dictionary to manage cancel states
cancel_broadcast = {}

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_users(client, message):
    global cancel_broadcast
    
    is_forward = False
    if len(message.command) > 1 and message.command[1] == "-f":
        is_forward = True
        mode_text = "Forward"
    else:
        mode_text = "Copy"
    
    broadcast_id = f"{message.chat.id}_{message.id}"
    cancel_broadcast[broadcast_id] = False
    
    # Cancel button
    cancel_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛑 Cancel Broadcast", callback_data=f"cancel_bc_{broadcast_id}")]
    ])
    
    msg = await message.reply(
        f"╭── ˹ {mode_text.upper()} BROADCAST ˼ ──\n"
        f"│\n"
        f"├─ 🔄 Mode: {mode_text}\n"
        f"├─ 📊 Progress: 0%\n"
        f"├─ ✅ Success: 0\n"
        f"├─ ❌ Failed: 0\n"
        f"╰─ 👥 Total: 0",
        reply_markup=cancel_btn,
        quote=True
    )
    
    users = await db.get_all_users()
    total_users = await db.users.count_documents({})
    
    count = 0
    failed = 0
    last_update_time = time.time()
    
    async for user in users:
        # Check if cancel was requested
        if cancel_broadcast.get(broadcast_id, False):
            await msg.edit(
                f"╭── ˹ {mode_text.upper()} BROADCAST ˼ ──\n"
                f"│\n"
                f"├─ 🔄 Mode: {mode_text}\n"
                f"├─ 🛑 **Cancelled by admin**\n"
                f"├─ ✅ Success: {count}\n"
                f"├─ ❌ Failed: {failed}\n"
                f"╰─ 👥 Total: {count + failed}",
                reply_markup=None
            )
            cancel_broadcast.pop(broadcast_id, None)
            return
        
        try:
            if is_forward:
                await message.reply_to_message.forward(user['_id'])
            else:
                await message.reply_to_message.copy(user['_id'])
            count += 1
        except Exception:
            failed += 1
        
        await asyncio.sleep(0.05)
        
        # Update progress every 5 seconds
        if time.time() - last_update_time >= 5:
            try:
                percentage = round(((count + failed) / total_users) * 100, 1) if total_users > 0 else 0
                await msg.edit(
                    f"╭── ˹ {mode_text.upper()} BROADCAST ˼ ──\n"
                    f"│\n"
                    f"├─ 🔄 Mode: {mode_text}\n"
                    f"├─ 📊 Progress: {percentage}%\n"
                    f"├─ ✅ Success: {count}\n"
                    f"├─ ❌ Failed: {failed}\n"
                    f"╰─ 👥 Total: {count + failed}",
                    reply_markup=cancel_btn
                )
                last_update_time = time.time()
            except:
                pass
    
    # Broadcast completed
    percentage = 100
    await msg.edit(
        f"╭── ˹ {mode_text.upper()} BROADCAST ˼ ──\n"
        f"│\n"
        f"├─ 🔄 Mode: {mode_text}\n"
        f"├─ 📊 Progress: {percentage}%\n"
        f"├─ ✅ Success: {count}\n"
        f"├─ ❌ Failed: {failed}\n"
        f"╰─ 👥 Total: {count + failed}\n\n"
        f"<blockquote>✅ **Broadcast completed!**\n📫 Sent to: {count}\n🚫 Failed: {failed}</blockquote>",
        reply_markup=None
    )
    
    cancel_broadcast.pop(broadcast_id, None)


@Client.on_message(filters.command("broadcast_groups") & filters.user(ADMINS) & filters.reply)
async def broadcast_groups(client, message):
    global cancel_broadcast
    
    broadcast_id = f"groups_{message.chat.id}_{message.id}"
    cancel_broadcast[broadcast_id] = False
    
    cancel_btn = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛑 Cancel Broadcast", callback_data=f"cancel_bc_{broadcast_id}")]
    ])
    
    msg = await message.reply(
        "╭── ˹ GROUPS BROADCAST ˼ ──\n"
        "│\n"
        "├─ 🔄 Mode: Copy\n"
        "├─ 📊 Progress: 0%\n"
        "├─ ✅ Success: 0\n"
        "├─ ❌ Failed: 0\n"
        "╰─ 👥 Total: 0",
        reply_markup=cancel_btn,
        quote=True
    )
    
    groups = await db.get_all_groups()
    total_groups = await db.groups.count_documents({})
    
    count = 0
    failed = 0
    last_update_time = time.time()
    
    async for group in groups:
        # Check if cancel was requested
        if cancel_broadcast.get(broadcast_id, False):
            await msg.edit(
                "╭── ˹ GROUPS BROADCAST ˼ ──\n"
                "│\n"
                "├─ 🔄 Mode: Copy\n"
                "├─ 🛑 **Cancelled by admin**\n"
                f"├─ ✅ Success: {count}\n"
                f"├─ ❌ Failed: {failed}\n"
                f"╰─ 👥 Total: {count + failed}",
                reply_markup=None
            )
            cancel_broadcast.pop(broadcast_id, None)
            return
        
        try:
            await message.reply_to_message.copy(group['_id'])
            count += 1
        except Exception:
            failed += 1
        
        await asyncio.sleep(0.05)
        
        if time.time() - last_update_time >= 5:
            try:
                percentage = round(((count + failed) / total_groups) * 100, 1) if total_groups > 0 else 0
                await msg.edit(
                    "╭── ˹ GROUPS BROADCAST ˼ ──\n"
                    "│\n"
                    "├─ 🔄 Mode: Copy\n"
                    f"├─ 📊 Progress: {percentage}%\n"
                    f"├─ ✅ Success: {count}\n"
                    f"├─ ❌ Failed: {failed}\n"
                    f"╰─ 👥 Total: {count + failed}",
                    reply_markup=cancel_btn
                )
                last_update_time = time.time()
            except:
                pass
    
    await msg.edit(
        "╭── ˹ GROUPS BROADCAST ˼ ──\n"
        "│\n"
        "├─ 🔄 Mode: Copy\n"
        "├─ 📊 Progress: 100%\n"
        f"├─ ✅ Success: {count}\n"
        f"├─ ❌ Failed: {failed}\n"
        f"╰─ 👥 Total: {count + failed}\n\n"
        f"<blockquote>✅ **Group broadcast completed!**\n📫 Sent to: {count}\n🚫 Failed: {failed}</blockquote>",
        reply_markup=None
    )
    
    cancel_broadcast.pop(broadcast_id, None)


# Handle cancel button click
@Client.on_callback_query(filters.regex(r"^cancel_bc_"))
async def cancel_broadcast_callback(client, query):
    broadcast_id = query.data.replace("cancel_bc_", "")
    if broadcast_id in cancel_broadcast:
        cancel_broadcast[broadcast_id] = True
        await query.answer("🛑 Broadcast cancelled! Stopping...", show_alert=True)
        await query.message.edit_reply_markup(reply_markup=None)
    else:
        await query.answer("Broadcast already finished or not active.", show_alert=True)
