from disnake.ext import commands

import os
import sys
import subprocess
from config import *
from db import *

bot = commands.Bot(test_guilds=[GUILD_ID])


async def check_admin_and_respond_if_not(inter):
    if not inter.author.get_role(ADMIN_ROLE_ID):
        await inter.response.send_message(
            "You do not have permission to run this command."
        )
        return False
    return True


def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    sys.stdout.flush()


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != RULES_MESSAGE_ID:
        return
    if payload.emoji.name == REACTION_EMOJI:
        member = payload.member
        guild = bot.get_guild(payload.guild_id)
        role = guild.get_role(ROLE_ID)

        await member.add_roles(role)

        name = f"{member.nick} ({member.name})" if member.nick else member.name
        print_flush(f"Added {name} to {role.name}")


@bot.slash_command()
async def server(inter):
    """
    Get server stats.
    """

    await inter.response.send_message(
        f"Server name: {inter.guild.name}\nTotal members: {inter.guild.member_count}"
    )


@bot.slash_command()
async def anonymous(inter, message):
    """
    Send an anonymous message to the board.

    Parameters
    ----------
    message: The message to send
    """

    channel = bot.get_channel(ANONYMOUS_MSGS_CHANNEL_ID)
    await channel.send(message)
    await inter.response.send_message("Sent.")
    await inter.delete_original_message()
    await inter.author.send("Your anonymous message has been sent to the board.")

    print_flush("Sent anonymous message")


@bot.slash_command()
async def refresh_website(inter):
    """
    Update the website with the latest changes (must be a board member to activate).
    """

    if not await check_admin_and_respond_if_not(inter):
        return

    print_flush("Refreshing website...")

    await inter.response.send_message("Refreshing website from Notion (eta ~5 mins)...")

    response = subprocess.run(
        ["/home/p/ps/psab/loconotion/update.sh"],
        capture_output=True,
    )

    content = (
        "Website refreshed successfully."
        if response.returncode == 0
        else f"Website refresh failed with exit code {response.returncode}. Check system log for details."
    )
    await inter.edit_original_message(content=content)

    print_flush(content)
    if response.returncode != 0:
        print_flush("website refresh stdout:", response.stdout.decode())
        print_flush("website refresh stderr:", response.stderr.decode())


@bot.slash_command()
async def birthday(inter, birthday):
    """
    Set your birthday so you can be celebrated by the computer overlords.

    Parameters
    ----------
    birthday: Your birthday in the format MM/DD/YYYY
    """

    if not birthday or not BIRTHDAY_REGEX.match(birthday.strip()):
        return await inter.response.send_message(
            "Invalid birthday format. Please use MM/DD/YYYY."
        )
    birthday = birthday.strip()

    user = inter.author.mention
    set_birthday(user, birthday)

    print_flush(f"Saved birthday for {user}: {birthday}")
    await inter.response.send_message(f"Set your birthday to {birthday}.")


bot.run(TOKEN)
