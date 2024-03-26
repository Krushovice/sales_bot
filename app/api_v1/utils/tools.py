from aiogram.types import Message

from app.api_v1.orm import User


def get_subscribe_info(user: User) -> dict:
    info = {}

    sub_date = user.expiration_date

    if user.subscription:
        info["subscribe"] = f"Активна до {sub_date}"

    else:
        info["subscribe"] = "Не активна"

    discount = user.discount

    if discount and discount > 0:
        info["discount"] = discount

    else:
        info["discount"] = "Нет"

    return info


def check_for_referral(message: Message) -> int:
    target = str(message.text)[6:]
    referral_id = int(target)
    return referral_id
