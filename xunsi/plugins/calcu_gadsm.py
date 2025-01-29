from .GADSM import GADSM

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment, Bot
from nonebot.params import CommandArg
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText

from nonebot_plugin_waiter import waiter

# 辅助函数，用于等待用户输入
async def get_user_response(bot: Bot, event: Event, timeout: int = 30) -> str:
    # 等待用户输入回复
    @waiter(waits=["message"])
    async def check(event1: Event):
        if event.get_session_id() == event1.get_session_id():
            return event1.get_plaintext()
    async for resp in check(timeout=timeout):
        return resp
    
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
    priority=4,
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
    prompt="""请直接发送GADSM计算参数：
格式：“[借力顺序] [出发年份] [到达年份] [初始C3]”
参数用空格分隔，借力天体编号为
1水星；2金星；3地球；4火星；5木星；6土星；7天王星；8海王星
如参数“235 2015 2020 30”的含义是
引力弹弓借力序列：金星-地球-土星，2015年出发，2020年到达土星，初始C3=30km²/s²""",
)
async def calcu_gadsm_function(bot: Bot, event: Event, gadsm_arg: str = ArgPlainText()):
    gadsm_arg_list = gadsm_arg.split(" ")
    required_fields = ["借力顺序", "出发年份", "到达年份", "初始C3"]
    current_params = [""] * 4

    # 填充现有参数
    for i in range(len(gadsm_arg_list)):
        current_params[i] = gadsm_arg_list[i]

    # 循环检查缺失的参数
    for i in range(len(current_params)):
        if current_params[i] == "":
            await calcu_gadsm.send(f"你输入的参数不足，请补充输入{required_fields[i]}：")
            user_input = await get_user_response(bot, event)

            # 检查用户输入是否为数字（借力顺序可以为多个数字）
            if i == 0:
                # 借力顺序检查是否只包含1-8
                if not all(char.isdigit() and 1 <= int(char) <= 8 for char in user_input):
                    await calcu_gadsm.finish("你在乱输什么参数？不干了！\ntips: 借力顺序输入错误！请确保包含1-8之间的天体编号。")
                current_params[i] = user_input
            else:
                # 检查其他输入项是否为数字
                if not user_input.isdigit():
                    await calcu_gadsm.finish(f"你在乱输什么东西？不干了！\ntips: {required_fields[i]}输入错误！请输入有效数字。")
                current_params[i] = user_input

    # 参数验证完成后，将参数赋值并进行计算
    sequence = [int(num) for num in current_params[0]]
    year_0 = int(current_params[1])
    year_1 = int(current_params[2])
    C_3 = float(current_params[3])

    # 检查年份是否符合条件
    if year_0 >= year_1:
        await calcu_gadsm.finish("到达时间怎么能够比出发时间还早的？不干了！\ntips:出发年份必须小于到达年份，请重新检查输入的年份！")

    result = GADSM.GADSM(sequence, year_0, year_1, C_3)
    
    await calcu_gadsm.finish(
        MessageSegment.at(event.get_user_id())
        + MessageSegment.text(f"您本次的计算参数和结果为:\n{result[0]}")
        + MessageSegment.image(
            f"file:///C:\\Users\\Administrator\\shiinano\\xunsi\\plugins\\GADSM\\GADSM\\{resalt[1]}"
        )
        + MessageSegment.text("该功能仅供娱乐，请不要使用该结果用于星际旅行哦！")
    )
