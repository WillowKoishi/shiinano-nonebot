from nonebot import on_command,on_notice
from nonebot.adapters.onebot.v11 import  Event,Message,MessageSegment,PokeNotifyEvent
from nonebot.params import CommandArg
from nonebot.rule import Rule,to_me
import random 

hello_test = on_command("存活测试2",priority=10,block=True)
upsetkoishi_trigger = on_command("倒立恋恋",aliases={"倒立恋恋2022"},priority=10,block=True)
upsetkoishi_trigger2 = on_command("倒立恋恋2",aliases={"倒立恋恋2024"},priority=10,block=True)


@hello_test.handle()
async def hello_test_method(event:Event,arg:Message=CommandArg()):
    msg = arg.extract_plain_text()
    await hello_test.finish("已打赢复活赛"+msg)

@upsetkoishi_trigger.handle()
async def upsetkoishi_function(event:Event):

    await upsetkoishi_trigger.finish(MessageSegment.at(event.get_user_id())+MessageSegment.image("file:///C:\\Users\\Administrator\\shiinano\\src\\img\\misc\\upsetkoishi_flag.png")+MessageSegment.image("file:///C:\\Users\\Administrator\\shiinano\\src\\img\\misc\\upsetkoishi.jpeg"))

@upsetkoishi_trigger2.handle()
async def upsetkoishi_function2(event:Event):
        await upsetkoishi_trigger.finish(MessageSegment.at(event.get_user_id())+MessageSegment.image("file:///C:\\Users\\Administrator\\shiinano\\src\\img\\misc\\upsetkoishi_flag2.png")+MessageSegment.text("2024.10.4我们拭目以待"))

poke_shiinano_trigger = on_notice(rule=to_me(),priority=4,block=True)
import os
@poke_shiinano_trigger.handle()
async def poke_shiinano_function(event:PokeNotifyEvent):
    voice_list = os.listdir("C:\\Users\\Administrator\\shiinano\\src\\audio\\pock_eff")
    print(voice_list)
    send_voice = f"file:///C:\\Users\\Administrator\\shiinano\\src\\audio\\pock_eff\\"+random.choice(voice_list)
    print(send_voice)
    rnd_flag = random.randint(1,10)
    if rnd_flag<2:
        await poke_shiinano_trigger.finish(MessageSegment.at(event.get_user_id())+" 不要揉我！")
    await poke_shiinano_trigger.finish(MessageSegment.record(send_voice))
    #await poke_shiinano_trigger.finish(Message(f'[CQ:poke,qq={event.get_user_id()}]'))