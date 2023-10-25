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
    weekend = (list(filter(lambda d: d.date.isoweekday() == 6 or d.date.isoweekday() == 7, holiday.all_days)))
    print("len(weekend)",len(weekend))

    working_weekend = []
    for d in holiday.all_days:
        isoweekday = d.date.isoweekday()
        if (isoweekday == 6 or isoweekday == 7) and not d.is_off:
            working_weekend.append(d)
    assert len(working_weekend) == 8
    
    normal_weekend = list(filter(lambda d: d.data is None, weekend))
    special_weekend = list(filter(lambda d: d.data is not None, weekend))
    rest_weekend = list(filter(lambda d: d.is_off, weekend))
    public_holiday = list(filter(lambda d: d.is_off and d.data is not None, holiday.all_days))
    print('len normal_weekend', len(normal_weekend), 'len(special_weekend)',len(special_weekend), 'len(rest_weekend)', len(rest_weekend), 
          'len(public_holiday)', len(public_holiday)
          )
    
    # assert len(holiday.holidays) == len(rest_weekend) + len

    # # assert len(holiday.workdays) == 243

    

