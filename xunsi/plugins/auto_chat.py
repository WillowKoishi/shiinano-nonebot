from nonebot import on_command,on_message
from nonebot.adapters.onebot.v11 import Event,Message,MessageSegment,MessageEvent
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.rule import Rule,to_me
#import redis

#时间和存储
import time,datetime
import pymysql
from nonebot import require

from nonebot.adapters.onebot.v11 import GroupMessageEvent
from nonebot.adapters import Bot

#redis_db = redis.StrictRedis(host='fairingstudio.com',port=6379,db=1,password="51445218lcy")
time_last_conn = 0

conn = pymysql.connect(host="fairingstudio.com",user="kuayue",password="114514KuaYue")#,database="kuayue")
cursor = conn.cursor()

def conn_sql():
    conn = pymysql.connect(host="fairingstudio.com",user="kuayue",password="114514KuaYue")#,database="kuayue")
    cursor = conn.cursor()


sqltest_trigger = on_command("sql测试",priority=10,block=True)

@sqltest_trigger.handle()
async def sqltest_function(event:Event,arg:Message=CommandArg()):
    global time_last_conn
    time_step1= time.time()
    if (time.time()-time_last_conn) >  7200:
        conn_sql()
        time_last_conn = time.time()
        logger.info(f"last conn update!!!!")


    msg = arg.extract_plain_text()
    if event.get_user_id() != "1033855007":
        #await sqltest_trigger.send()
        return
    if msg =="1":
        cursor.execute("show databases")
        logger.info(f"execute使用时间：{time.time()-time_step1}")

        callback_data = cursor.fetchall()
        logger.info(f"fetchall使用时间：{time.time()-time_step1}")

        await sqltest_trigger.send(str(callback_data))
        logger.info(f"sending msg使用时间：{time.time()-time_step1}")
    elif msg == "2":
        sql_serv_info = conn.get_server_info()
        logger.info(f"get服务器信息使用时间:{time.time()-time_step1}")
        await sqltest_trigger.send(str(sql_serv_info))
        logger.info(f"sending msg使用时间：{time.time()-time_step1}")

    elif msg =="3":
        cursor.execute("use kuayue")
        cursor.execute("show tables")
        logger.info(f"execute使用时间：{time.time()-time_step1}")

        callback_data = cursor.fetchall()
        logger.info(f"fetchall使用时间：{time.time()-time_step1}")

        await sqltest_trigger.send(str(callback_data))
        logger.info(f"sending msg使用时间：{time.time()-time_step1}")
    elif msg =="4":
        await sqltest_trigger.send()
    else:
        await sqltest_trigger.send()
    
    using_time =(time.time())- (time_step1 )
    logger.info(f"查询结束时间{time.time()}")
    await sqltest_trigger.finish(f"消耗时间：{using_time}")

typo_to_char={"柳树怪","LM51"}
async def contains_typo_key(event:MessageEvent) ->bool:
    text = event.get_plaintext()
    for typo in typo_to_char:
        if typo in text:
            return True
    return False

#learning_chat_trigger = on_message(priority=10,block=False)#,rule=Rule(contains_typo_key))

# @learning_chat_trigger.handle()
# async def learning_chat_function(bot: Bot, event2: GroupMessageEvent,event:GroupMessageEvent,arg:Message=CommandArg()):
#     #logger.info(learning_chat_trigger.rule())
#     logger.info(f"[111]on_message echo test userif={event.get_user_id()},session_id={event.get_session_id()},plaintext={event.get_plaintext()}")
#     if event.get_user_id() == "1033855007":
#         logger.info(f"[222]on_message echo test userif={event.get_user_id()},session_id={event.get_session_id()},plaintext={event.get_plaintext()}")
#         await learning_chat_trigger.finish(event.get_plaintext())
#     else:
#         logger.info(f"[333]on_message echo test userif={event.get_user_id()},session_id={event.get_session_id()},plaintext={event.get_plaintext()}")
#         await learning_chat_trigger.finish()

group_message = on_message(priority=10, block=False)

@group_message.handle()
async def handle_group_message(bot: Bot, event: GroupMessageEvent):
    msg = event.get_plaintext()
    if str(event.group_id) == '589943678':
        if event.get_user_id() == '1033855007':
            #await group_message.send(msg)
            logger.info(event.get_event_description())    
    else:
        logger.info(f"invalid user id,msg:'{msg}'")
        return