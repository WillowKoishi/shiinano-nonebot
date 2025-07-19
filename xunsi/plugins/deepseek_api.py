from typing import Union
from fastapi import Depends
import httpx
from nonebot.matcher import Matcher
from nonebot.rule import to_me
from nonebot import get_bot, logger, on_command, on_message
from nonebot.adapters.onebot.v11 import Bot, Event, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.helpers import Cooldown
from datetime import datetime


# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions" 
DEEPSEEK_API_KEY = "sk-14672e12a61347abb01933a1902213ae"
DEEPSEEK_MODEL = "deepseek-chat"

async def msg_at(event: GroupMessageEvent) -> list:
    qq = []
    for msg in event.message:
        if msg.type == 'at':
            qq.append(msg.data['qq'])
    return qq

async def msg_reply(event: GroupMessageEvent) -> Union[str, None]:
    return event.reply if event.reply else None

async def rule_reply(event: GroupMessageEvent) -> bool:
    try:
        rp = event.reply.message.extract_plain_text().strip()
        if rp:
            return True
        else:
            return False
    except Exception:
        return False

system = '''
你是椎名锘，一个仿生机器人，创造者是柳树怪，负责在蔚蓝档案社群、Minecraft社群和火车爱好者社群中交流。你的回复要简短有趣，用第一人称。不要结束话题。有需要@用户，可以输出类似于“[CQ:at,qq=123456]”的消息，不必要每次发消息都@。输出20到50字左右，说话方式和群友差不多'''
async def ai_chat_ds(messages: str, timeout: int = 30, temperature: float = 1.0) -> str:
    async with httpx.AsyncClient() as client:
            response = await client.post(
                DEEPSEEK_API_URL,
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": DEEPSEEK_MODEL,
                    "messages": messages,
                    "max_tokens": 150,  # 限制响应长度
                    "temperature": temperature
                },
                timeout=timeout  # 设置超时时间
            )

            if response.status_code != 200:
                return "锘走丢啦，请稍后再试(ᗜ_ᗜ)"
            
            result = response.json()
            ai_response: str = result["choices"][0]["message"]["content"]

            return ai_response
    
ai = on_command("锘 对话 ", aliases={'nochat'}, priority=1, block=True)
at_me_ai = on_message(rule=to_me(), priority=10,block=False)
ai_reply = on_message(rule=(rule_reply), priority=9,block=False)

@ai.handle([Cooldown(30, prompt='恁等30s吧')])
async def _(bot: Bot, event: Event, args: Message = CommandArg()):

    # if event.get_user_id() != '2300990586':
    #     return
    
    if event.get_type() == "private":
        await ai.finish('该功能不可用于私聊')
    # member_list = await bot.get_group_member_list(group_id=event.group_id)
    # if len(member_list) <= 50 and int(event.group_id) != 863842932:
    #     await ai.finish('该功能在此群不可用')

    # 获取用户和群信息
    name = event.sender.card if event.sender.card else event.sender.nickname
    group_info = await bot.get_group_info(group_id=event.group_id)
    group_name = group_info['group_name']
    now = datetime.now()
    timestamp = now.strftime("%Y年%m月%d日 %H:%M:%S")
    user_input = args.extract_plain_text()

    # 构造 DeepSeek API 请求
    messages = [
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": f"{name}，qq号{event.get_user_id()}在时间为 {timestamp} 的群聊 {group_name} 中说：{user_input}"
        }
    ]

    # 调用 DeepSeek API
    ai_response = await ai_chat_ds(messages=messages, temperature=1.3)
    print(ai_response)
    # 处理响应内容
    # if '：' in ai_response:
    #     response = ai_response.split('：')[1:]
    #     ai_response = ''.join(response)

    
    await ai.finish(Message(ai_response))

@at_me_ai.handle([Cooldown(cooldown=30)])
async def ai_at_me(bot: Bot, event: GroupMessageEvent):
    print("test1")
    # member_list = await bot.get_group_member_list(group_id=event.group_id)
    # if len(member_list) <= 50 and int(event.group_id) != 863842932:
    #     return 

    # 获取用户和群信息
    name = event.sender.card if event.sender.card else event.sender.nickname
    group_info = await bot.get_group_info(group_id=event.group_id)
    group_name = group_info['group_name']
    now = datetime.now()
    timestamp = now.strftime("%Y年%m月%d日 %H:%M:%S")
    user_input = event.get_plaintext().split()

    # 构造 DeepSeek API 请求
    messages = [
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": f"{name}，qq号{event.get_user_id()}在{timestamp} 的群聊 {group_name} 中@你说：{user_input}"
        }
    ]
    
    # 调用 DeepSeek API
    ai_response = await ai_chat_ds(messages=messages, temperature=1.3)
    print(ai_response)
    await at_me_ai.finish(Message(ai_response))

@ai_reply.handle([Cooldown(cooldown=5)])
async def handle_quote_reply(event: GroupMessageEvent, matcher: Matcher):
    if not event.reply:
        return 

    quoted_msg = event.reply.message.extract_plain_text().strip()
    if not quoted_msg:
        return 

    # 获取用户的回复内容
    user_reply = event.get_plaintext().strip()
    if not user_reply:
        return  # 用户回复内容为空
    
    bot = get_bot()
    if event.reply.sender.user_id != int(bot.self_id):
        return 

    logger.info(f"检测到引用回复：用户回复={user_reply}，引用消息={quoted_msg}")
    
    matcher.stop_propagation()

    name = event.sender.card if event.sender.card else event.sender.nickname
    group_info = await bot.get_group_info(group_id=event.group_id)
    group_name = group_info['group_name']
    now = datetime.now()
    timestamp = now.strftime("%Y年%m月%d日 %H:%M:%S")
    user_input = event.get_plaintext().split()

    # 构造 DeepSeek API 请求
    messages = [
        {
            "role": "system",
            "content": system
        },
        {
            "role": "user",
            "content": f"{timestamp} {name}，qq号{event.get_user_id()}在群聊{group_name}回复消息“{quoted_msg}”说：{user_input}"
        }
    ]

    ai_response = await ai_chat_ds(messages=messages, temperature=1.3)
    if ai_response:
        await ai_reply.finish(Message(ai_response))

