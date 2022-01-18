import sys
from config import ADMIN_ROLE_ID


def print_flush(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


async def check_admin_and_respond_if_not(inter):
    if not inter.author.get_role(ADMIN_ROLE_ID):
        await inter.response.send_message(
            "You do not have permission to run this command."
        )
        return False
    return True
