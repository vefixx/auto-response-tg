from datetime import datetime, timedelta

from telethon.sync import TelegramClient, events


api_id = 0
api_hash = ''
phone = ''
owner_username = ""
reply_message = ""

client = TelegramClient(phone, api_id, api_hash)

temp = {}


@client.on(events.NewMessage)
async def handler(event):
    global temp
    sender = await event.get_sender()

    if sender.username == owner_username:
        return

    if sender.username not in temp:
        temp[sender.username] = {}
        temp[sender.username]["last_reply_date"] = None

    if event.is_private:

        # Проверка, что сообщение отправляется первый раз за сессию скрипта.
        if temp[sender.username]["last_reply_date"] is None:
            await event.reply(reply_message)
            temp[sender.username]["last_reply_date"] = datetime.now()
            return

        # Проверка, что с последнего ответа прошло больше часа и диалог неактивный в течение часа.
        if datetime.now() - temp[sender.username]["last_reply_date"] > timedelta(hours=1):

            # Проверяем, что диалог активен.
            async for message in client.iter_messages(event.chat_id):
                sender_entity = await client.get_entity(message.sender_id)

                # Проверяем, что сообщение является нашим.
                if sender_entity.username == owner_username:

                    # Если наше последнее сообщение было отправлено час назад.
                    if datetime.now() - message.date > timedelta(hours=1):
                        await event.reply(reply_message)
                        temp[sender.username]["last_reply_date"] = datetime.now()
                    break
            return


async def main():
    await client.connect()
    await client.run_until_disconnected()


if __name__ == '__main__':
    with client:
        client.loop.run_until_complete(main())
