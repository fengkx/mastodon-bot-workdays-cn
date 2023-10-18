import httpx

from mastodon_bot.holidays.model import HolidayData


async def get_holidays_data(year: int) -> HolidayData:
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"https://cdn.jsdelivr.net/gh/NateScarlet/holiday-cn@master/{year}.json"
        )
        holidayData = HolidayData.model_validate_json(r.text)
        return holidayData
