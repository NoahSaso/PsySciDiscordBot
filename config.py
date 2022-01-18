import os
from dotenv import load_dotenv
import re

load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

ANONYMOUS_MSGS_CHANNEL_ID = int(os.getenv("ANONYMOUS_MSGS_CHANNEL_ID"))

ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))

RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID"))
REACTION_EMOJI = os.getenv("REACTION_EMOJI")
REACTION_ROLE_ID = int(os.getenv("REACTION_ROLE_ID"))

MAIN_CHANNEL_ID = int(os.getenv("MAIN_CHANNEL_ID"))

BIRTHDAY_PICKLE_FILE = os.path.join(
    os.path.dirname(__file__), os.getenv("BIRTHDAY_PICKLE_FILE", "birthday.p")
)
BIRTHDAY_REGEX = re.compile(r"^\d{2}\/\d{2}$")
