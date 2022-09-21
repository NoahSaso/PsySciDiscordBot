import sys
from config import ADMIN_ROLE_IDS


def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


async def check_admin_and_respond_if_not(inter):
    if not any(inter.author.get_role(role_id) for role_id in ADMIN_ROLE_IDS):
        await inter.response.send_message(
            "You do not have permission to run this command."
        )
        return False
    return True
