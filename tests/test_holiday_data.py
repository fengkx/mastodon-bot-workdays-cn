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


@pytest.mark.asyncio
async def test_holiday_data_2024():
    holiday = await HolidayDataByYear.create(2024)
    assert len(holiday.all_days) == 366

    assert len(holiday.all_days) == len(holiday.holidays) + len(holiday.workdays)
    weekend = list(
        filter(
            lambda d: d.date.isoweekday() == 6 or d.date.isoweekday() == 7,
            holiday.all_days,
        )
    )
    assert len(weekend) == 104
    print("len(workdays)=", len(holiday.workdays))
    public_holiday = len(list(filter(lambda d: d.data is not None, holiday.holidays)))
    print("len(public_holidays)", public_holiday)
    print("len(holidays)=", len(holiday.holidays))
    assert len(holiday.holidays) == 115
    assert len(holiday.workdays) == 251
