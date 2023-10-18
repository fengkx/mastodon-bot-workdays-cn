import os
import asyncio
from typing import Optional
from zoneinfo import ZoneInfo
from datetime import datetime
import textwrap

from environs import Env
from mastodon import Mastodon  # type: ignore

from mastodon_bot.holidays import HolidayDataByYear
from mastodon_bot.holidays.date import DateWithWithData


env = Env()


class Bot:
    holidayData: HolidayDataByYear
    mastodon: Optional[Mastodon]
    debug: bool
    dry_run: bool
    check_last_sent: bool

    @classmethod
    async def init(
        cls,
        *,
        debug: bool = False,
        access_token: Optional[str],
        api_base_url: Optional[str],
        dry_run: bool = False,
        check_last_sent=True,
    ):
        self = Bot()
        now = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        current_year = now.year

        self.holidayData = await HolidayDataByYear.create(current_year)
        self.debug = debug
        self.dry_run = dry_run
        self.check_last_sent = check_last_sent
        if api_base_url is not None and access_token is not None:
            self.mastodon = Mastodon(
                access_token=access_token, api_base_url=api_base_url
            )
        return self

    def make_toot(self) -> str:
        now = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
        today = self.holidayData.get_date(now.date())
        if today.is_off:
            return self.make_holiday_toot(today)
        return self.make_workday_toot(today)

    def make_workday_toot(self, d: DateWithWithData) -> str:
        next_holiday = self.holidayData.next_holiday(d.date)
        if next_holiday is not None:
            interval = next_holiday.date - d.date
        remain_workday_cnt = self.holidayData.remain_workdays(d.date)

        result = f"""\
        今天是工作日，{f"距离下一个假期还有{interval.days}天" if next_holiday is not None else "今年已经没有假期了"}。
        {f"今年总共有{len(self.holidayData.workdays)}天工作日，算上今天还剩{remain_workday_cnt}天。" if remain_workday_cnt > 0 else "今年的班就上到这了！"}
        """
        return textwrap.dedent(result)

    def make_holiday_toot(self, d: DateWithWithData) -> str:
        next_workday = self.holidayData.next_workday(d.date)
        if next_workday is not None:
            interval = next_workday.date - d.date
        remain_holiday_cnt = self.holidayData.remain_holidays(d.date)

        result = f"""\
        今天是{d.reason}，{f"距离下一个工作日还有{interval.days}天" if next_workday is not None else "今年已经没有工作日了"}。
        {f"今年总共有{len(self.holidayData.holidays)}天假期，算上今天还剩{remain_holiday_cnt}天假期。" if remain_holiday_cnt > 0 else "今年已经没有假期了！"}
        """
        return textwrap.dedent(result)

    def toot(self):
        if self.mastodon is None:
            return
        toot = self.make_toot()

        if self.dry_run is False:
            last_sent_path = os.path.join(
                os.path.dirname(__file__), "../../auto/.last_sent_at"
            )
            with open(
                last_sent_path,
                "r+",
            ) as f:
                now = datetime.now(tz=ZoneInfo("Asia/Shanghai"))
                try:
                    last_sent = datetime.fromisoformat(f.read())
                except Exception as exp:
                    print(exp)
                    last_sent = None

                if (
                    self.check_last_sent
                    and last_sent is not None
                    and now.date() == last_sent.date()
                ):
                    return
                self.mastodon.status_post(
                    status=toot,
                    visibility="public" if self.debug else "unlisted",
                    language="zh",
                )
                f.seek(0)
                f.write(now.replace(microsecond=0).isoformat())
        print(f"{toot} | {datetime.now()}")


async def run():
    debug = env.bool("DEBUG", False)
    api_base_url = env.str("MSTDN_API_BASE_URL", None)
    access_token = env.str("MSTDN_ACCESS_TOKEN", None)
    dry_run = env.bool("MSTDN_DRY_RUN", False)
    check_last_sent = env.bool("CHECK_LAST_SENT", True)
    bot = await Bot.init(
        debug=debug,
        api_base_url=api_base_url,
        access_token=access_token,
        dry_run=dry_run,
        check_last_sent=check_last_sent,
    )
    bot.toot()


def main():
    # Read .env into os.environ
    env.read_env()
    asyncio.run(run())
