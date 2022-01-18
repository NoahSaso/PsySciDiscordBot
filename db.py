import pickle
import os
from filelock import FileLock
from config import BIRTHDAY_PICKLE_FILE, BIRTHDAY_PICKLE_FILE_LOCK

# Safely write to pickle file.
# We need this because in order to write to the pickle file, we first read the entire dict into memory. Then, we set the appropriate key and subsequently write the entire dict back to the pickle file. This reading and writing is not atomic, so we need to lock the file.
lock = FileLock(BIRTHDAY_PICKLE_FILE_LOCK)


def ensure_birthday_file_exists():
    """
    Create the file if it doesn't exist and save an empty dict
    """

    if not os.path.exists(BIRTHDAY_PICKLE_FILE):
        with open(BIRTHDAY_PICKLE_FILE, "wb") as f:
            pickle.dump({}, f)


def set_birthday(user, birthday):
    with lock:
        ensure_birthday_file_exists()

        birthdays = pickle.load(open(BIRTHDAY_PICKLE_FILE, "rb"))
        birthdays[user] = birthday
        pickle.dump(birthdays, open(BIRTHDAY_PICKLE_FILE, "wb"))


def get_birthdays():
    with lock:
        ensure_birthday_file_exists()

        birthdays = pickle.load(open(BIRTHDAY_PICKLE_FILE, "rb"))
        return birthdays


get_birthday = lambda user: get_birthdays().get(user)
