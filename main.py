from telethon import TelegramClient, events

api_id = 31891006  # <-- apna api_id daal
api_hash = '79068ae528aa4242c45006cb68c89a07' # <-- apna api_hash daal

import os

session_name = os.getenv("SESSION_NAME", "session")

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


client.start()
print("🔥 Bot chal raha hai...")
client.run_until_disconnected()