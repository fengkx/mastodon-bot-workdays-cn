import pytest
from mastodon_bot.holidays import HolidayDataByYear


@pytest.mark.asyncio
async def test_holiday_data():
    holiday = await HolidayDataByYear.create(2023)
    assert len(holiday.all_days) == 365
