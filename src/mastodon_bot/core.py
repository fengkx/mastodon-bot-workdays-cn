import asyncio
from zoneinfo import ZoneInfo
from datetime import datetime, date
import textwrap


from mastodon_bot.holidays import HolidayDataByYear
from mastodon_bot.holidays.date import DateWithWithData

class Bot:
    holidayData: HolidayDataByYear
    @classmethod
    async def init(cls):
        self = Bot()
        now = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        current_year = now.year

        self.holidayData = await HolidayDataByYear.create(current_year)
        return self
    
    def make_toot(self) -> str:
        now = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        today = self.holidayData.get_date(now.date())
        if today.is_off:
            return self.make_holiday_toot( today)
        return self.make_workday_toot(today)
    
    def make_workday_toot(self, d: DateWithWithData) -> str:
        next_holiday = self.holidayData.next_holiday(d.date)
        interval = next_holiday.date - d.date
        remain_holiday_cnt = self.holidayData.remain_holidays(d.date)
        
        result = f"""\
        今天是工作日，距离下一个假期还有{interval.days}天
        {f"今年总共有{len(self.holidayData.holidays)}天假期，还剩{remain_holiday_cnt}天假期" if remain_holiday_cnt > 0 else "今年已经没有假期了！"}
        """
        return textwrap.dedent(result)

    def make_holiday_toot(self, d: DateWithWithData) -> str:
        next_workday = self.holidayData.next_workday(d.date)
        interval = next_workday.date - d.date
        remain_holiday_cnt = self.holidayData.remain_holidays(d.date)

        result = f"""\
        今天是{d.reason}，距离下一个工作日还有{interval.days}天
        {f"今年总共有{len(self.holidayData.holidays)}天假期，还剩{remain_holiday_cnt}天假期" if remain_holiday_cnt > 0 else "今年已经没有假期了！"}
        """
        return textwrap.dedent(result)

async def run():
    bot = await Bot.init()
    print(bot.make_toot())
    


def main():
    asyncio.run(run())