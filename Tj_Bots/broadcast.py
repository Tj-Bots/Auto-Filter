from pyrogram import Client, filters
from config import ADMINS
from database import db
import asyncio
import time
import json
import os

# Store broadcast messages for editing/deleting (until restart)
BROADCAST_STORAGE = {}
BROADCAST_FILE = "broadcast_storage.json"

# Load saved broadcasts if file exists
def load_broadcast_storage():
    global BROADCAST_STORAGE
    if os.path.exists(BROADCAST_FILE):
        try:
            with open(BROADCAST_FILE, 'r') as f:
                BROADCAST_STORAGE = json.load(f)
        except:
            BROADCAST_STORAGE = {}

def save_broadcast_storage():
    with open(BROADCAST_FILE, 'w') as f:
        json.dump(BROADCAST_STORAGE, f)

load_broadcast_storage()

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS))
async def broadcast_command(client, message):
    # Check if replying to a message
    if not message.reply_to_message:
        # Handle delete/edit without reply
        args = message.text.split()
        if len(args) >= 2:
            broadcast_id = args[1]
            
            # Delete broadcast: -d or --delete
            if len(args) >= 3 and (args[2] == "-d" or args[2] == "--delete"):
                if broadcast_id in BROADCAST_STORAGE:
                    del BROADCAST_STORAGE[broadcast_id]
                    save_broadcast_storage()
                    await message.reply(f"✅ Broadcast `{broadcast_id}` deleted.", quote=True)
                else:
                    await message.reply(f"❌ Broadcast `{broadcast_id}` not found.", quote=True)
                return
        else:
            await message.reply(
                "**📢 Broadcast Commands:**\n\n"
                "• Reply to a message with `/broadcast` - Send to users\n"
                "• `/broadcast -f` (reply) - Forward to users\n"
                "• `/broadcast -q` (reply) - Quiet broadcast (no status updates)\n"
                "• `/broadcast -q -f` (reply) - Quiet forward broadcast\n"
                "• `/broadcast [ID] -e` (reply to edited msg) - Edit broadcast\n"
                "• `/broadcast [ID] -d` - Delete broadcast\n\n"
                "**Flags:**\n"
                "`-f, --forward` - Forward instead of copy\n"
                "`-q, --quiet` - No status message updates\n"
                "`-e, --edit` - Edit existing broadcast\n"
                "`-d, --delete` - Delete broadcast",
                quote=True
            )
        return
    
    args = message.command[1:] if len(message.command) > 1 else []
    is_forward = False
    is_quiet = False
    is_edit = False
    broadcast_id = None
    
    # Parse flags
    for arg in args:
        if arg in ["-f", "--forward"]:
            is_forward = True
        elif arg in ["-q", "--quiet"]:
            is_quiet = True
        elif arg in ["-e", "--edit"]:
            is_edit = True
        elif arg in ["-d", "--delete"]:
            # Delete is handled separately above
            pass
        elif not arg.startswith("-"):
            broadcast_id = arg
    
    # Handle edit mode
    if is_edit and broadcast_id:
        if broadcast_id not in BROADCAST_STORAGE:
            await message.reply(f"❌ Broadcast `{broadcast_id}` not found.", quote=True)
            return
        
        original_sender = BROADCAST_STORAGE[broadcast_id].get('sender_id')
        if original_sender != message.from_user.id:
            await message.reply("❌ You can only edit your own broadcasts.", quote=True)
            return
        
        # Store the new message info for editing
        BROADCAST_STORAGE[broadcast_id]['edit_chat_id'] = message.chat.id
        BROADCAST_STORAGE[broadcast_id]['edit_message_id'] = message.reply_to_message.id
        save_broadcast_storage()
        
        await message.reply(f"✅ Broadcast `{broadcast_id}` ready for edit. Use `/broadcast` to send the updated version.", quote=True)
        return
    
    # Generate broadcast ID
    if not broadcast_id:
        broadcast_id = str(int(time.time()))
    
    msg_text = ""
    if not is_quiet:
        msg_text = "🚀 Starting broadcast..."
        if is_forward:
            msg_text = "🚀 Starting broadcast (Forward)..."
    
    status_msg = None
    if not is_quiet:
        status_msg = await message.reply(msg_text, quote=True)
    
    users = await db.get_all_users()
    
    count = 0
    failed = 0
    last_update_time = time.time()
    
    # Store broadcast info for future editing
    BROADCAST_STORAGE[broadcast_id] = {
        'is_forward': is_forward,
        'sender_id': message.from_user.id,
        'chat_id': message.chat.id,
        'reply_msg_id': message.reply_to_message.id,
        'timestamp': broadcast_id
    }
    save_broadcast_storage()
    
    async for user in users:
        try:
            if is_forward:
                await message.reply_to_message.forward(user['_id'])
            else:
                await message.reply_to_message.copy(user['_id'])
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
            
        if not is_quiet and time.time() - last_update_time >= 5:
            try:
                await status_msg.edit(f"⏳ Broadcasting to users...\n✅ Sent: {count}\n🚫 Failed: {failed}")
                last_update_time = time.time()
            except:
                pass
    
    if not is_quiet:
        await status_msg.edit(f"✅ **User broadcast completed.**\n\n📫 Sent to: {count}\n🚫 Failed/Blocked: {failed}\n🆔 Broadcast ID: `{broadcast_id}`")
    else:
        await message.reply(f"✅ **User broadcast completed.**\n\n📫 Sent to: {count}\n🚫 Failed/Blocked: {failed}\n🆔 Broadcast ID: `{broadcast_id}`", quote=True)

@Client.on_message(filters.command("broadcast_groups") & filters.user(ADMINS))
async def broadcast_groups(client, message):
    # Check if replying to a message
    if not message.reply_to_message:
        await message.reply(
            "**📢 Group Broadcast:**\n\n"
            "Reply to a message with `/broadcast_groups` to send to all groups.\n\n"
            "**Flags:**\n"
            "`-f, --forward` - Forward instead of copy\n"
            "`-q, --quiet` - No status message updates",
            quote=True
        )
        return
    
    args = message.command[1:] if len(message.command) > 1 else []
    is_forward = False
    is_quiet = False
    
    for arg in args:
        if arg in ["-f", "--forward"]:
            is_forward = True
        elif arg in ["-q", "--quiet"]:
            is_quiet = True
    
    msg = None
    if not is_quiet:
        msg = await message.reply("🚀 Starting group broadcast...", quote=True)
    
    groups = await db.get_all_groups()
    
    count = 0
    failed = 0
    last_update_time = time.time()
    
    async for group in groups:
        try:
            if is_forward:
                await message.reply_to_message.forward(group['_id'])
            else:
                await message.reply_to_message.copy(group['_id'])
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
            
        if not is_quiet and time.time() - last_update_time >= 5:
            try:
                await msg.edit(f"⏳ Broadcasting to groups...\n✅ Sent: {count}\n🚫 Failed: {failed}")
                last_update_time = time.time()
            except:
                pass
    
    if not is_quiet:
        await msg.edit(f"✅ **Group broadcast completed.**\n\n📫 Sent to: {count}\n🚫 Failed: {failed}")
    else:
        await message.reply(f"✅ **Group broadcast completed.**\n\n📫 Sent to: {count}\n🚫 Failed: {failed}", quote=True)

# Command to edit a broadcast message after it's been sent
@Client.on_message(filters.command("edit_broadcast") & filters.user(ADMINS))
async def edit_broadcast_message(client, message):
    args = message.command
    if len(args) < 2:
        await message.reply("Usage: `/edit_broadcast [broadcast_id]` (reply to the new message)", quote=True)
        return
    
    broadcast_id = args[1]
    
    if broadcast_id not in BROADCAST_STORAGE:
        await message.reply(f"❌ Broadcast `{broadcast_id}` not found.", quote=True)
        return
    
    if not message.reply_to_message:
        await message.reply("❌ Reply to the new message you want to replace it with.", quote=True)
        return
    
    broadcast_data = BROADCAST_STORAGE[broadcast_id]
    is_forward = broadcast_data.get('is_forward', False)
    
    users = await db.get_all_users()
    count = 0
    failed = 0
    
    status_msg = await message.reply(f"✏️ Editing broadcast `{broadcast_id}`...", quote=True)
    
    async for user in users:
        try:
            if is_forward:
                await message.reply_to_message.forward(user['_id'])
            else:
                await message.reply_to_message.copy(user['_id'])
            count += 1
            await asyncio.sleep(0.05)
        except Exception:
            failed += 1
    
    await status_msg.edit(f"✅ **Broadcast edit completed.**\n\n📫 Sent to: {count}\n🚫 Failed: {failed}")
