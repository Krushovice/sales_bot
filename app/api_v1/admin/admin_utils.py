import datetime
from app.api_v1.orm import User


def show_users_statistic(users: list[User]) -> dict:
    users_info = {
        "count_users": 0,
        "active_users": 0,
        "subs_today": 0,
        "inactive": 0,
    }
    today = datetime.datetime.now().date()
    for user in users:
        users_info["count_users"] += 1
        if user.subscription:
            users_info["active_users"] += 1
            sub_date = datetime.datetime.strptime(
                user.subscribe_date,
                "%d-%m-%Y",
            ).date()
            if sub_date == today:
                users_info["subs_today"] += 1

        users_info["today"] = today.strftime("%d-%m-%Y")
        users_info["inactive"] = users_info["count_users"] - users_info["active_users"]
    return users_info
