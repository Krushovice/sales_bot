from datetime import datetime

from app.api_v1.core import AsyncOrm


async def check_user_expiration(tg_id: int):
    user = await AsyncOrm.get_user(tg_id=tg_id)

    if user.subscription:
        current_date = datetime.now()
        expiration_date = datetime.strptime(user.expiration_date, "%Y-%m-%d")
        delta = expiration_date - current_date
        if 0 < delta.days <= 3:
            return True
    return False
