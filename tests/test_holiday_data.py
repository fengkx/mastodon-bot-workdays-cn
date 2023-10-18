import pytest
from mastodon_bot.holidays import HolidayDataByYear
from datetime import date


@pytest.mark.asyncio
async def test_holiday_data():
    holiday = await HolidayDataByYear.create(2023)
    assert len(holiday.all_days) == 365

    d = holiday.get_date(date(2023, 10, 7))
    assert d.is_off is False
    assert "国庆节" in d.reason and "补班" in d.reason

    # should count current day
    assert holiday.remain_holidays(date(2023, 1, 1)) == len(holiday.holidays)

    assert len(holiday.all_days) == len(holiday.holidays) + len(holiday.workdays)

    assert len(holiday.all_days) == 365
