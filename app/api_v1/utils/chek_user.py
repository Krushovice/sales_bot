from app.api_v1.core import AsyncOrm


async def check_user(tg_id: int):
    user = await AsyncOrm.get_user(tg_id=tg_id)
    if user.key:
        return user
    return None
