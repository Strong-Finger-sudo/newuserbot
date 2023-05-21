#main imports
from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import Message
from pyrogram import filters

#base imports
import random
import asyncio
import datetime

import random_choise
#local imports
import settings
import synonymizer

api_id = int(settings.BOT_ID)
api_hash = str(settings.BOT_HASH)

client = Client(name='my_client', api_id=api_id, api_hash=api_hash, proxy=settings.proxy_data)

now = str(datetime.datetime.now().time())[:8]

from_time = str(input("From time - ")) #С какого времени будет проводиться рассылка
to_time = str(input("To time - ")) #По какое время будет проводиться рассылка

from_time_sec = (int(from_time[:2]) * 3600 ) + (int(from_time[3:5]) * 60)
to_time_sec = (int(to_time[:2]) * 3600 ) + (int(to_time[3:5]) * 60)

total_secs = to_time_sec - from_time_sec

first_message = random.randint(int((total_secs // 4) * 0.9), int((total_secs // 4) * 1.1))
second_message = random.randint(int((total_secs // 4) * 0.9), int((total_secs // 4) * 1.1)) + first_message
third_message = random.randint(int((total_secs // 4) * 0.9), int((total_secs // 4) * 1.1)) + second_message
fourth_message = to_time_sec - 1

async def invite_users(client: Client, message: Message):
    if message.text == "startProcess":
        print(1)
        from_time_sec = (int(from_time[:2]) * 3600) + (int(from_time[3:5]) * 60)
        to_time_sec = (int(to_time[:2]) * 3600) + (int(to_time[3:5]) * 60)

        count = 0

        while True:
            print(2)
            now = str(datetime.datetime.now().time())[:8]
            now_sec = (int(now[:2]) * 3600) + (int(now[3:5]) * 60) + (int(now[6:]))

            while from_time_sec < now_sec < to_time_sec:
                print(3)
                now = str(datetime.datetime.now().time())[:8]
                now_sec = (int(now[:2]) * 3600) + (int(now[3:5]) * 60) + (int(now[6:]))

                if now_sec == from_time_sec + first_message or now_sec == from_time_sec + second_message or now_sec == from_time_sec + third_message or now_sec == fourth_message:
                    print(4)
                    with open("chats.txt", "r") as chats:

                        for chat in chats:

                            try:
                                link = await client.create_chat_invite_link(chat_id=message.chat.id)
                            except:
                                await client.send_message(chat_id=chat, text=f"Couldn't form invitation link")

                            try:
                                await client.send_message(chat_id=chat, text=f"{synonymizer.synonymize(synonymizer.synonymize(random_choise.random_choise(settings.INVITATION_TEXT)))}\n{link.invite_link}")
                            except:
                                await client.send_message(chat_id=chat, text=f"Couldn't send invitation to this chat - {chat}")

                                count += 1

                            # changing proxy every 5 message
                            if count % 5 == 0:

                                with open("proxies.txt", "r") as proxies:

                                    for proxy in proxies:

                                        if proxy[:13] != settings.proxy_data['hostname']:

                                            settings.proxy_data['hostname'] = proxy[:13]
                                            settings.proxy_data['port'] = int(proxy[14:])

                                            count = 0

                                            break
                await asyncio.sleep(1)
            await asyncio.sleep(1)
            if now_sec > to_time_sec:
                break

client.add_handler(MessageHandler(invite_users, filters=filters.text))

client.run()