from typing import Optional, TypeAlias, Union
from functools import cached_property

from mastodon_bot.holidays.get_holidays_data import get_holidays_data
from mastodon_bot.holidays.date import DateWithWithData
from mastodon_bot.holidays.model import Day
from datetime import date, datetime
from dateutil import rrule

TDate: TypeAlias = Day


class HolidayDataByYear:
    year: int
    _map: dict[str, TDate]

    @classmethod
    async def create(cls, year: int):
        self = HolidayDataByYear()
        self.year = year
        data = await get_holidays_data(year)
        self._map = {day.date: day for day in data.days}

        return self

    def get_date(self, d: Union[date, datetime]) -> DateWithWithData:
        date_str = f"{d.year:02d}-{d.month:02d}-{d.day:02d}"
        data = self._map.get(date_str)

        return DateWithWithData(year=d.year, month=d.month, day=d.day, data=data)

    @cached_property
    def all_days(self) -> list[DateWithWithData]:
        daily_in_year = rrule.rrule(
            rrule.DAILY,
            dtstart=datetime(year=self.year, month=1, day=1),
            until=datetime(year=self.year, month=12, day=31),
        )
        dates = [self.get_date(dt) for dt in daily_in_year]
        return dates

    @cached_property
    def holidays(self) -> list[DateWithWithData]:
        return list(filter(lambda d: d.is_off, self.all_days))

    @cached_property
    def workdays(self) -> list[DateWithWithData]:
        return list(filter(lambda d: not d.is_off, self.all_days))

    def next_holiday(self, d: date) -> Optional[DateWithWithData]:
        for holiday in self.holidays:
            if holiday.date > d:
                return holiday
        return None

    def next_workday(self, d: date) -> Optional[DateWithWithData]:
        for workday in self.workdays:
            if workday.date > d:
                return workday
        return None

    def remain_holidays(self, d: date) -> int:
        """包含 |d| 今年还剩有多少天假"""
        return len(list(filter(lambda holiday: holiday.date >= d, self.holidays)))

    def remain_workdays(self, d: date) -> int:
        """包含 |d| 今年还剩有多少天工作日"""
        return len(list(filter(lambda workday: workday.date >= d, self.workdays)))
