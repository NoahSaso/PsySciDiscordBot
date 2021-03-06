from disnake.ext import commands

import sys
import subprocess
from config import *
from db import *
from util import *
from datetime import datetime
import logging
import traceback

bot = commands.Bot(test_guilds=[GUILD_ID])


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
        role = guild.get_role(REACTION_ROLE_ID)

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

    try:
        if not await check_admin_and_respond_if_not(inter):
            return

        start = datetime.now()
        print_flush("Refreshing website...")

        await inter.response.send_message(
            "Refreshing website from Notion (will update this message once done)..."
        )
        # Obtain the message ID so we can update it after a long time.
        # Editing the message via the interaction fails after a while.
        # I think the token expires, so the followup webhook is necessary.
        msg_id = (await inter.original_message()).id

        response = subprocess.Popen(
            ["/home/p/ps/psab/loconotion/update.sh"],
            stdout=subprocess.PIPE,
        )
        for c in iter(lambda: response.stdout.read(1), b""):
            sys.stdout.buffer.write(c)
            sys.stdout.buffer.flush()
        returncode = response.wait()

        end = datetime.now()

        time_string = f"started {start.strftime('%H:%M:%S')}, ended {end.strftime('%H:%M:%S')}, took {end - start}"

        content = (
            f"Website refreshed successfully. ({time_string})"
            if returncode == 0
            else f"Website refresh failed with exit code {returncode}. Check system log for details. ({time_string})"
        )
        await bot.get_message(msg_id).edit(content=content)

        print_flush(content)
    except Exception as e:
        print_flush(f"Failed to refresh website: {e}")
        logging.error(traceback.format_exc())


@bot.slash_command()
async def birthday(inter, birthday):
    """
    Set your birthday so you can be celebrated by the computer overlords.

    Parameters
    ----------
    birthday: Your birthday in the MM/DD format
    """

    if not birthday or not BIRTHDAY_REGEX.match(birthday.strip()):
        return await inter.response.send_message(
            "Invalid birthday format. Please use MM/DD."
        )
    birthday = birthday.strip()

    user = inter.author.mention
    set_birthday(user, birthday)

    print_flush(f"Saved birthday for {user}: {birthday}")
    await inter.response.send_message(f"Set your birthday to {birthday}.")


bot.run(TOKEN)
