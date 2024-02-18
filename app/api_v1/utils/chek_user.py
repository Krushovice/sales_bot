import datetime

from app.api_v1 import AsyncOrm


async def check_user_expiration(tg_id: int):
    user = await AsyncOrm.get_user(tg_id=tg_id)

    if user.subscription:
        current_date = datetime.datetime.today()
        delta = current_date - user.expiration_date
        if 0 < delta <= 3:
            return True
    return False
