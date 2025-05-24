import asyncio
import aiohttp
from loguru import logger


class RandomUsersAPI:
    MAX_RETRIES = 3

    @classmethod
    async def get_users(cls, count: int | None = 1000) -> dict | None:
        url = "https://randomuser.me/api/"
        params = {"results": f"{count}"}
        for attempt in range(1, cls.MAX_RETRIES + 1):
            session = aiohttp.ClientSession()
            try:
                async with session.get(url=url, params=params, ssl=False) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.success(f"Data got successful on attempt {attempt}")
                        await session.close()
                        return data
                    else:
                        logger.warning(
                            f"Data get failed (status={response.status}) on attempt {attempt}"
                        )
                        await session.close()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                logger.error(f"Attempt {attempt} failed with error: {e}")
                await session.close()
