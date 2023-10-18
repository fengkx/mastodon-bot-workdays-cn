import pytest
from mastodon_bot.core import Bot
from datetime import date, datetime
from zoneinfo import ZoneInfo
from freezegun import freeze_time


def mock_datetime_now_by(dt: datetime):
    @pytest.fixture
    def mock_datetime_now(mocker):
        now = dt
        # 使用freezegun库来冻结时间
        frozen_time = freeze_time(now)
        frozen_time.start()
        yield now
        frozen_time.stop()

    return mock_datetime_now


mock1 = mock_datetime_now_by(
    datetime(
        year=2023,
        month=10,
        day=17,
        hour=9,
        minute=0,
        second=0,
        tzinfo=ZoneInfo("Asia/Shanghai"),
    )
)
@pytest.mark.asyncio
async def test_bot_1(mock1):
    bot = await Bot.init(dry_run=True)
    txt = bot.make_toot()
    assert "下一个假期还有4天" in txt
    assert "今天是工作日" in txt
    assert "算上今天还剩54天" in txt


mock2 = mock_datetime_now_by(
    datetime(
        year=2023,
        month=10,
        day=1,
        hour=9,
        minute=0,
        second=0,
        tzinfo=ZoneInfo("Asia/Shanghai"),
    )
)
@pytest.mark.asyncio
async def test_bot_2(mock2):
    bot = await Bot.init(dry_run=True)
    txt = bot.make_toot()
    assert "下一个工作日还有6天" in txt
    assert "国庆节" in txt
    assert "算上今天还剩30天假期" in txt



mock3 = mock_datetime_now_by(
    datetime(
        year=2023,
        month=10,
        day=7,
        hour=9,
        minute=0,
        second=0,
        tzinfo=ZoneInfo("Asia/Shanghai"),
    )
)
@pytest.mark.asyncio
async def test_bot_3(mock3):
    bot = await Bot.init(dry_run=True)
    txt = bot.make_toot()
    assert "国庆节补班" in txt
    assert "下一个假期还有7天" in txt
    assert "算上今天还剩62天" in txt



mock4 = mock_datetime_now_by(
    datetime(
        year=2023,
        month=12,
        day=29,
        hour=9,
        minute=0,
        second=0,
        tzinfo=ZoneInfo("Asia/Shanghai"),
    )
)
@pytest.mark.asyncio
async def test_bot_4(mock4):
    bot = await Bot.init(dry_run=True)
    txt = bot.make_toot()
    assert "今天是工作日" in txt
    assert "下一个假期还有1天" in txt
    assert "算上今天还剩1天" in txt


mock5 = mock_datetime_now_by(
    datetime(
        year=2023,
        month=12,
        day=31,
        hour=9,
        minute=0,
        second=0,
        tzinfo=ZoneInfo("Asia/Shanghai"),
    )
)
@pytest.mark.asyncio
async def test_bot_4(mock5):
    bot = await Bot.init(dry_run=True)
    txt = bot.make_toot()
    assert "今天是休息日" in txt
    assert "今年已经没有工作日了" in txt
    assert "算上今天还剩1天假期" in txt

