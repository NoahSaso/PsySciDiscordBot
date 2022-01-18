import pickle
import os
from config import BIRTHDAY_PICKLE_FILE


def ensure_birthday_file_exists():
    """
    Create the file if it doesn't exist and save an empty dict
    """

    if not os.path.exists(BIRTHDAY_PICKLE_FILE):
        with open(BIRTHDAY_PICKLE_FILE, "wb") as f:
            pickle.dump({}, f)


def set_birthday(user, birthday):
    ensure_birthday_file_exists()
    birthdays = pickle.load(open(BIRTHDAY_PICKLE_FILE, "rb"))
    birthdays[user] = birthday
    pickle.dump(birthdays, open(BIRTHDAY_PICKLE_FILE, "wb"))


def get_birthday(user):
    ensure_birthday_file_exists()
    birthdays = pickle.load(open(BIRTHDAY_PICKLE_FILE, "rb"))
    return birthdays.get(user)
