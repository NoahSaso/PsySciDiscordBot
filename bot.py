import disnake
from disnake.ext import commands

import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

RULES_MESSAGE_ID = int(os.getenv('RULES_MESSAGE_ID'))
REACTION_EMOJI = os.getenv('REACTION_EMOJI')
ROLE_ID = int(os.getenv('ROLE_ID'))

ANONYMOUS_MSGS_CHANNEL_ID = int(os.getenv('ANONYMOUS_MSGS_CHANNEL_ID'))

ADMIN_ROLE_ID = int(os.getenv('ADMIN_ROLE_ID'))

bot = commands.Bot(test_guilds=[GUILD_ID])

async def check_admin_and_respond_if_not(inter):
    if not inter.author.get_role(ADMIN_ROLE_ID):
        await inter.response.send_message("You do not have permission to run this command.")
        return False
    return True

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
        print(f"Added {name} to {role.name}")
        sys.stdout.flush()

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

    print("Sent anonymous message")
    sys.stdout.flush()

@bot.slash_command()
async def refresh_website(inter):
    """
    Update the website with the latest changes (must be a board member to activate).
    """

    if not await check_admin_and_respond_if_not(inter):
        return

    print("Refreshing website...")
    sys.stdout.flush()

    await inter.response.send_message("Refreshing website from Notion (eta ~5 mins)...")
    
    response = subprocess.run(["/home/p/ps/psab/loconotion/update.sh"], capture_output=True)

    content = "Website refreshed successfully." if response.returncode == 0 else f"Website refresh failed with exit code {response.returncode}. Check system log for details."
    await inter.edit_original_message(content=content)
    
    print(content)
    if response.returncode != 0:
        print('website refresh stdout:', response.stdout.decode())
        print('website refresh stderr:', response.stderr.decode())
    sys.stdout.flush()

bot.run(TOKEN)
