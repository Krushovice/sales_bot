def get_user_info(user) -> dict:
    info = {}
    sub_date = user.expiration_date
    if user.subscription:
        info["sub_info"] = f"Активна до {sub_date}"
    info["sub_info"] = "Не активна"

    discount = user.discount

    if discount and discount > 0:
        info["discount"] = discount

    else:
        info["discount"] = "Нет"

    return info
