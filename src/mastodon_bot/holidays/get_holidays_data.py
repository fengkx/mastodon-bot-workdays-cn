from typing import Optional
import httpx

from mastodon_bot.holidays.model import HolidayData


async def get_holidays_data(year: int) -> Optional[HolidayData]:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
        )
        if r.is_error:
            return None
        holidayData = HolidayData.model_validate_json(r.text)
        return holidayData
