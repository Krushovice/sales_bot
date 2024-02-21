import datetime
import asyncio
from app.api_v1.core.crud import AsyncOrm
from app.api_v1.utils.request_api import outline_helper


async def main():
    while True:
        users = await AsyncOrm.get_users_by_subscription()

        current_time = datetime.datetime.now().strftime("%Y-%m-%d")

        for user in users:
            if current_time >= user.expiration_date:
                if user.key:
                    print(user.key.id)
                    await outline_helper.set_key_limit(key_id=user.key.api_id)

        # Ждем определенное время перед следующей проверкой
        await asyncio.sleep(3600)  # Проверка каждый час


if __name__ == "__main__":
    asyncio.run(main())
