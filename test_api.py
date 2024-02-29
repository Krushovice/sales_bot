import datetime
import asyncio
from app.api_v1.core.crud import AsyncOrm
from app.api_v1.utils.requests.request_api import outline_helper


async def main():
    async with AsyncOrm() as orm:
        outline_helper(orm)


if __name__ == "__main__":
    asyncio.run(main())
