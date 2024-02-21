import asyncio
import datetime


from app.api_v1.core.crud import AsyncOrm

from app.api_v1.utils.request_api import outline_helper


async def check_subscription_expiry():
    try:
        users = await AsyncOrm.get_users_by_subscription()

        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        for user in users:
            if current_date >= user.expiration_date:
                if user.key:
                    await outline_helper.set_key_limit(key_id=user.key.api_id)

    except Exception as e:
        print(f"An error occurred in check_subscription_expiry: {e}")

    # После завершения проверок подписок, планируем новую задачу через некоторое время
    asyncio.create_task(schedule_next_check())


async def schedule_next_check():
    await asyncio.sleep(3600)  # Проверка каждый час
    asyncio.create_task(check_subscription_expiry())
