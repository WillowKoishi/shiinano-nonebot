from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment
from nonebot.params import CommandArg

# 数学
import matplotlib.pyplot as plt
import random
import numpy as np

# 时间和存储
import time, datetime
import redis
from nonebot import require

require("nonebot_plugin_localstore")
import toml


from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment

database_token = toml.load("C:\\Users\\Administrator\\shiinano\\database_tocken.toml")
redis_db = redis.StrictRedis(
    host=database_token["redis_database"]["host"],
    port=database_token["redis_database"]["port"],
    db=1,
    password=database_token["redis_database"]["pswd"],
)


today_length_trigger = on_command(
    "今日长度", aliases={"jrcd", "金日成的"}, priority=10, block=True
)
yesterday_length_trigger = on_command(
    "昨日长度", aliases={"zrcd"}, priority=10, block=True
)
avg_length_trigger = on_command("平均长度", priority=10, block=True)
tester = on_command("数据库测试", priority=10, block=True)


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    yesterdaystr = yesterday.strftime("%Y%m%d")
    return yesterdaystr


@today_length_trigger.handle()
async def today_length_function(event: Event, arg: Message = CommandArg()):
    print(event.get_session_id())
    print(event.get_session_id().find("809238483"))
    if not event.get_session_id().find("809238483"):
        await today_length_trigger.finish()
    time_today = time.localtime(time.time())
    data = np.random.normal(12, 7, 100)
    logger.info(data)
    is_ident = True
    while is_ident:
        random_seg = round(random.choice(data), 2)
        if random_seg > 13 or random_seg < 0:
            is_ident = False
    
    user_id = event.get_user_id()
    timestep = time.strftime("%Y%m%d")

    before_length = redis_db.hget(f"length:{user_id}", f"{timestep}")
    if before_length == None:
        redis_db.hmset(f"length:{user_id}", {f"{timestep}": random_seg})
    else:
        random_seg = float(before_length)

    if random_seg <= 0:
        await today_length_trigger.finish(
            MessageSegment.at(event.get_user_id())
            + "今日你的长度....今日你是女孩子（"
            + str(random_seg)
            + "cm）"
        )
    else:
        await today_length_trigger.finish(
            MessageSegment.at(event.get_user_id())
            + "今日你的长度是:"
            + str(random_seg)
            + "cm"
        )


@yesterday_length_trigger.handle()
async def yestoday_length_function(event: Event):
    user_id = event.get_user_id()
    yesterday = getYesterday()
    before_length = redis_db.hget(f"length:{user_id}", f"{yesterday}")
    if before_length:
        if float(before_length) >= 0:
            await yesterday_length_trigger.finish(
                MessageSegment.at(event.get_user_id())
                + " 昨日你的长度是:"
                + str(before_length, encoding="utf8")
                + "cm"
            )
        else:
            await yesterday_length_trigger.finish(
                MessageSegment.at(event.get_user_id())
                + "昨日你的长度....昨天你是女孩子（"
                + str(before_length, encoding="utf8")
                + "cm)"
            )
    else:
        await yesterday_length_trigger.finish(
            MessageSegment.at(event.get_user_id()) + "未找到你昨日的长度记录！"
        )


@avg_length_trigger.handle()
async def avg_length_function(event: Event, arg: Message = CommandArg()):
    user_id = event.get_user_id()

    before_length_all = [float(i) for i in redis_db.hvals(f"length:{user_id}")]
    if len(before_length_all) == 0:
        await avg_length_trigger.finish(
            MessageSegment.at(event.get_user_id()) + " 未检索到你往日长度的任何记录！"
        )
    else:
        avg = round(sum(before_length_all) / len(before_length_all), 4)

        await avg_length_trigger.finish(
            MessageSegment.at(event.get_user_id())
            + f" 共检索到你的{len(before_length_all)}条记录,你的平均长度是{avg}cm"
        )


@tester.handle()
async def tester_trigger():
    redis_db.hmset(f"length:1033855007", {f"20241033": 12})
    await tester.finish(str(redis_db.ping()))
