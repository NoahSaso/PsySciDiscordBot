import asyncio
import disnake
import sys
import os
import traceback
from datetime import datetime

# parent dir
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from config import TOKEN, GUILD_ID, MAIN_CHANNEL_ID
from db import get_birthdays
from util import print_flush


async def wish(users):
    client = disnake.Client()
    try:
        await client.login(TOKEN)

        guild = await client.fetch_guild(GUILD_ID)
        channel = await guild.fetch_channel(MAIN_CHANNEL_ID)

        if how_many == 1:
            user_str = users[0]
        elif how_many == 2:
            user_str = f"{users[0]} and {users[1]}"
        else:
            user_str = ", ".join(users[:-1])
            user_str += f", and {users[-1]}"

        message = f":partying_face: Happy birthday to {user_str}! :partying_face:"
        await channel.send(message)
        print_flush(message)
    except Exception as e:
        print_flush(traceback.format_exc())
    finally:
        if not client.is_closed():
            await client.close()


if __name__ == "__main__":
    today = datetime.now().strftime("%m/%d")
    birthdays = get_birthdays()

    matching_users = [user for user, birthday in birthdays.items() if birthday == today]
    how_many = len(matching_users)

    if how_many > 0:
        asyncio.run(wish(matching_users))
