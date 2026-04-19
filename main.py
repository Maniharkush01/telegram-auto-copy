from telethon import TelegramClient, events
from telethon.errors import AuthKeyDuplicatedError

import os
import sys

api_id = 31891006  # <-- apna api_id daal
api_hash = '79068ae528aa4242c45006cb68c89a07' # <-- apna api_hash daal

session_name = os.getenv("SESSION_NAME", "session")
session_file = f"{session_name}.session"

# Delete a corrupted/duplicate session before starting if requested
if os.getenv("FORCE_NEW_SESSION", "").lower() in ("1", "true", "yes"):
    if os.path.exists(session_file):
        os.remove(session_file)
        print(f"⚠️  FORCE_NEW_SESSION: deleted '{session_file}'. Starting fresh.")

client = TelegramClient(session_name, api_id, api_hash)

source_group = '@theprofessionals'
target_group = '@kushjobs123'

message_map = {}

@client.on(events.NewMessage(chats=source_group))
async def new_message_handler(event):
    try:
        reply_to = None

        if event.is_reply:
            reply_msg = await event.get_reply_message()
            reply_to = message_map.get(reply_msg.id)

        sent = await event.message.copy_to(target_group, reply_to=reply_to)
        message_map[event.message.id] = sent.id

    except Exception as e:
        print("Error:", e)


@client.on(events.MessageEdited(chats=source_group))
async def edit_handler(event):
    try:
        if event.message.id in message_map:
            await client.edit_message(
                target_group,
                message_map[event.message.id],
                event.message.text or ""
            )
    except Exception as e:
        print("Edit error:", e)


phone = os.getenv("TELEGRAM_PHONE")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

if not phone and not bot_token:
    print(
        "❌ Missing credentials: set either TELEGRAM_PHONE (for a user account) "
        "or TELEGRAM_BOT_TOKEN (for a bot) as an environment variable."
    )
    sys.exit(1)

try:
    if bot_token:
        client.start(bot_token=bot_token)
    else:
        client.start(phone=phone)
except AuthKeyDuplicatedError:
    print(
        "❌ AuthKeyDuplicatedError: the session file is corrupted or was used "
        "from multiple IPs simultaneously. Deleting the session file now.\n"
        "➡️  Restart the app to create a fresh session."
    )
    if os.path.exists(session_file):
        os.remove(session_file)
    sys.exit(1)

print("🔥 Bot chal raha hai...")
client.run_until_disconnected()
