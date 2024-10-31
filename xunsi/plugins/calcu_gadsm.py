from xunsi.plugins.GADSM import GADSM

from nonebot import on_command, on_notice
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment, PokeNotifyEvent
from nonebot.params import CommandArg
from nonebot.rule import Rule, to_me
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText
import math
import numpy as np

gadsm_test = on_command("锘 GADSM测试", priority=10, block=True)
calcu_gadsm = on_command(
    "锘 GADSM",
    aliases={
        "锘 引力弹弓",
        "锘GADSM",
        "锘引力弹弓",
        "锘yldg",
        "锘 瞎几把飞",
        "锘瞎几把飞",
    },
    priority=10,
    block=True,
)


@gadsm_test.handle()
async def gadsm_test_method(event: Event, arg: Message = CommandArg()):
    if (event.get_user_id()) == "1033855007":
        resalt = GADSM.GADSM_demo()
        await gadsm_test.finish(
            MessageSegment.at(event.get_user_id())
            + MessageSegment.text(f"您本次的计算参数和结果为:\n{resalt[0]}")
            + MessageSegment.image(
                f"file:///C:\\Users\\Administrator\\shiinano\\xunsi\\plugins\\GADSM\\GADSM\\{resalt[1]}"
            )
        )
    await gadsm_test.finish("你不是bot的主人，不可以使用这个功能(")


@calcu_gadsm.handle()
def calcu_gadsm_trigger(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("gadsm_arg", args)


@calcu_gadsm.got(
    "gadsm_arg",
    prompt="""请输入GADSM计算参数：
格式：“[借力顺序][出发年份][到达年份][初始C3]”
参数用空格分隔，借力天体编号为
1水星；2金星；3地球；4火星；5木星；6土星；7天王星；8海王星
如参数“235 2015 2020 30”的含义是
引力弹弓借力序列：金星-地球-土星，2015年出发，2020年到达土星，初始C3=30km²/s²""",
)
async def calcu_gadsm_function(event: Event, gadsm_arg: str = ArgPlainText()):
    gadsm_arg_list = gadsm_arg.split(" ")
    print(gadsm_arg_list)
    sequence = gadsm_arg_list[0]
    year_0 = gadsm_arg_list[1]
    year_1 = gadsm_arg_list[2]
    C_3 = gadsm_arg_list[3]
    result = GADSM.GADSM(sequence, year_0, year_1, C_3)
    await calcu_gadsm.finish(
        MessageSegment.at(event.get_user_id())
        + MessageSegment.text(f"您本次的计算参数和结果为:\n{result[0]}")
        + MessageSegment.image(
            f"file:///C:\\Users\\Administrator\\shiinano\\xunsi\\plugins\\GADSM\\GADSM\\{result[1]}"
        )
        + MessageSegment.text("该功能仅供娱乐，请不要使用该结果用于星际旅行哦！")
    )
