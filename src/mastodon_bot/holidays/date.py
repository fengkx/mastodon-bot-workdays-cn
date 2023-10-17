import datetime
from dataclasses import dataclass
from datetime import date
from typing import Optional
from functools import cached_property

from mastodon_bot.holidays.model import Day

@dataclass
class DateWithWithData:
    date: datetime.date
    data: Optional[Day]
    def __init__(self, year: int, month: int, day: int, data: Optional[date]) -> None:
        self.date = date(year=year, month=month, day=day)
        self.data = data
    
    def is_special(self) -> bool:
        return self.data is not None

    @cached_property
    def is_off(self) -> bool:
        if self.data is None:
            isoweekday = self.date.isoweekday()
            return isoweekday == 6 or isoweekday == 7
        return self.data.isOffDay

    @cached_property
    def reason(self) -> str:
        if not self.is_special():
            return f"{'休息日' if self.is_off else '工作日'}"
        return f"{self.data.name}{'假期' if self.is_off else '补班'}"
    
    