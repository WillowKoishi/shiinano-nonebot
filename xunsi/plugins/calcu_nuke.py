#核瞎算
import numpy as np
import pandas as pd
from scipy.stats import linregress
from nonebot import on_command
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment, PokeNotifyEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText

# 数据定义：用于“球球”构型（如W87，长度120厘米）
ball_ball_data = {
    "Length_cm": [120, 105.5],
    "Width_cm": [35, 33.8],
    "Weight_kg": [270, 147],
    "Yield_kT": [475, 200]
}

# 定义“球柱”构型的数据（W80和MK49）
ball_cylinder_data = {
    "Length_cm": [80, 138],
    "Width_cm": [30, 51],
    "Weight_kg": [130, 740],
    "Yield_kT": [150, 1100]
}

# 执行线性回归以生成拟合参数
df_ball_ball = pd.DataFrame(ball_ball_data)
df_ball_cylinder = pd.DataFrame(ball_cylinder_data)

# “球球”构型的线性拟合
yield_weight_fit_ball_ball = linregress(df_ball_ball["Yield_kT"], df_ball_ball["Weight_kg"])
yield_length_fit_ball_ball = linregress(df_ball_ball["Yield_kT"], df_ball_ball["Length_cm"])
yield_width_fit_ball_ball = linregress(df_ball_ball["Yield_kT"], df_ball_ball["Width_cm"])

# “球柱”构型的线性拟合
yield_weight_fit_ball_cylinder = linregress(df_ball_cylinder["Yield_kT"], df_ball_cylinder["Weight_kg"])
yield_length_fit_ball_cylinder = linregress(df_ball_cylinder["Yield_kT"], df_ball_cylinder["Length_cm"])
yield_width_fit_ball_cylinder = linregress(df_ball_cylinder["Yield_kT"], df_ball_cylinder["Width_cm"])

# 杀伤半径计算
def calculate_kill_radius(yield_tons):
    """
    计算杀伤半径，单位为千米。
    公式：kill_radius_km = 1.493885 * (yield_tons)^(1/3)
    """
    return 1.493885 * (yield_tons ** (1/3))

# 核心计算函数
def calculate_parameters(config_type, known_value, known_type):
    """
    根据构型和已知单一指标计算其余指标。

    参数：
    config_type (str): 构型类型（"球球" 或 "球柱"）
    known_value (float): 已知指标值
    known_type (str): 已知指标类型（"当量"、"长度"、"宽度"、"重量"）

    返回：
    dict: 包含计算结果的字典，包括当量、重量、长度、宽度和杀伤半径
    """
    # 使用对应的构型系数
    if config_type == "球球":
        # 根据已知指标类型进行计算
        if known_type.find("当量"):
            yield_kT = known_value * 10000  # 将“万吨”转换为“千吨”
            weight = yield_weight_fit_ball_ball.slope * yield_kT + yield_weight_fit_ball_ball.intercept
            length = yield_length_fit_ball_ball.slope * yield_kT + yield_length_fit_ball_ball.intercept
            width = yield_width_fit_ball_ball.slope * yield_kT + yield_width_fit_ball_ball.intercept
        elif known_type.find("重量"):
            weight = known_value
            yield_kT = (weight - yield_weight_fit_ball_ball.intercept) / yield_weight_fit_ball_ball.slope
            length = yield_length_fit_ball_ball.slope * yield_kT + yield_length_fit_ball_ball.intercept
            width = yield_width_fit_ball_ball.slope * yield_kT + yield_width_fit_ball_ball.intercept
        elif known_type.find("长度"):
            length = known_value
            yield_kT = (length - yield_length_fit_ball_ball.intercept) / yield_length_fit_ball_ball.slope
            weight = yield_weight_fit_ball_ball.slope * yield_kT + yield_weight_fit_ball_ball.intercept
            width = yield_width_fit_ball_ball.slope * yield_kT + yield_width_fit_ball_ball.intercept
        elif known_type.find("宽度"):
            width = known_value
            yield_kT = (width - yield_width_fit_ball_ball.intercept) / yield_width_fit_ball_ball.slope
            weight = yield_weight_fit_ball_ball.slope * yield_kT + yield_weight_fit_ball_ball.intercept
            length = yield_length_fit_ball_ball.slope * yield_kT + yield_length_fit_ball_ball.intercept
        else:
            raise ValueError("无效的已知指标类型。请选择 '当量'、'长度'、'宽度' 或 '重量'。")

    elif config_type == "球柱":
        # 根据已知指标类型进行计算
        if known_type == "当量":
            yield_kT = known_value * 10000  # 将“万吨”转换为“千吨”
            weight = yield_weight_fit_ball_cylinder.slope * yield_kT + yield_weight_fit_ball_cylinder.intercept
            length = yield_length_fit_ball_cylinder.slope * yield_kT + yield_length_fit_ball_cylinder.intercept
            width = yield_width_fit_ball_cylinder.slope * yield_kT + yield_width_fit_ball_cylinder.intercept
        elif known_type == "重量":
            weight = known_value
            yield_kT = (weight - yield_weight_fit_ball_cylinder.intercept) / yield_weight_fit_ball_cylinder.slope
            length = yield_length_fit_ball_cylinder.slope * yield_kT + yield_length_fit_ball_cylinder.intercept
            width = yield_width_fit_ball_cylinder.slope * yield_kT + yield_width_fit_ball_cylinder.intercept
        elif known_type == "长度":
            length = known_value
            yield_kT = (length - yield_length_fit_ball_cylinder.intercept) / yield_length_fit_ball_cylinder.slope
            weight = yield_weight_fit_ball_cylinder.slope * yield_kT + yield_weight_fit_ball_cylinder.intercept
            width = yield_width_fit_ball_cylinder.slope * yield_kT + yield_width_fit_ball_cylinder.intercept
        elif known_type == "宽度":
            width = known_value
            yield_kT = (width - yield_width_fit_ball_cylinder.intercept) / yield_width_fit_ball_cylinder.slope
            weight = yield_weight_fit_ball_cylinder.slope * yield_kT + yield_weight_fit_ball_cylinder.intercept
            length = yield_length_fit_ball_cylinder.slope * yield_kT + yield_length_fit_ball_cylinder.intercept
        else:
            raise ValueError("无效的已知指标类型。请选择 '当量'、'长度'、'宽度' 或 '重量'。")

    else:
        raise ValueError("构型类型无效，仅支持 '球球' 和 '球柱' 构型。")

    # 杀伤半径计算
    yield_tons = yield_kT * 1000  # 转换为吨
    kill_radius = calculate_kill_radius(yield_tons)

    return f"""--核瞎算 计算结果--
当量: {yield_kT/10000}万吨
重量:{weight:.2f}kg
长度: {length:.2f}cm
宽度: {width:.2f}cm
杀伤半径: {kill_radius:.2f}km
温馨提示：计算纯属娱乐，请不要用于实际作战中！"""

# 示例：输入“球球 120万吨”以进行计算
config_type = "球球"
known_type = "当量"
known_value = 120  # 万吨

result = calculate_parameters(config_type, known_value, known_type)
print("计算结果:", result)



calcu_nuke = on_command("锘 核瞎算",priority=10,block=True)
@calcu_nuke.handle()
def _(matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text():
        matcher.set_arg("nuke_arg", args)


@calcu_nuke.got(
    "nuke_arg",
    prompt="""---核瞎算---
参数说明：[核武器构型] [已知数据] [数值]
武器构型目前支持：球球、球柱
已知数据支持:当量、长度、宽度、重量""",
)
async def _(event: Event, nuke_arg: str = ArgPlainText()):
    nuke_arg_list = nuke_arg.split(" ")
    print(nuke_arg_list)
    result = calculate_parameters(nuke_arg_list[0], float(nuke_arg_list[2]), nuke_arg_list[1])
    print(result)
    await calcu_nuke.finish(result)

