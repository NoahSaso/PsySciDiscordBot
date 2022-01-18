import os
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

RULES_MESSAGE_ID = int(os.getenv("RULES_MESSAGE_ID"))
REACTION_EMOJI = os.getenv("REACTION_EMOJI")
ROLE_ID = int(os.getenv("ROLE_ID"))

BIRTHDAY_PICKLE_FILE = os.getenv("BIRTHDAY_PICKLE_FILE", "birthday.p")
BIRTHDAY_REGEX = re.compile(r"^\d{2}\/\d{2}\/\d{4}$")
