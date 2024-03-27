from aiogram.types import Message

from app.api_v1.orm import User, AsyncOrm


async def count_active_referrals(tg_id: int) -> int:
    refs = await AsyncOrm.get_active_referrals(tg_id=tg_id)
    return len(refs)


async def get_subscribe_info(user: User) -> dict:
    info = {}

    sub_date = user.expiration_date

    if user.subscription:
        info["subscribe"] = f"Активна до {sub_date}"

    else:
        info["subscribe"] = "Не активна"

    discount = await count_active_referrals(user.tg_id)

    if discount and discount > 0:
        info["discount"] = discount

    else:
        info["discount"] = 0

    return info


def check_for_referral(message: Message) -> int:
    if len(message.text) > 6:
        target = str(message.text)[6:]
        referral_id = int(target)
        return referral_id
    return False
