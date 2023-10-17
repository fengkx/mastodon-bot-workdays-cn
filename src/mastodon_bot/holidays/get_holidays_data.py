import httpx
from pydantic.tools import parse_obj_as

from mastodon_bot.holidays.model import HolidayData

async def get_holidays_data(year: int) -> HolidayData:
    async with httpx.AsyncClient() as client:
        r = await client.get(f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json")
        holidayData = parse_obj_as(HolidayData, r.json())
        return holidayData

if (__name__ == '__main__'):
    import asyncio
    asyncio.run(get_holidays_data(2023))