from PIL import Image
from pysstv.color import MartinM2,PD90
from nonebot import on_command, on_message
from nonebot.adapters.onebot.v11 import Event, Message, MessageSegment, MessageEvent
from nonebot.params import CommandArg
from nonebot.log import logger
from nonebot.rule import Rule, to_me
import requests
from io import BytesIO
import time, datetime

from nonebot import require

def encode_sstv(image, output_audio_path):
    sstv = PD90(image,48000,16)
    sstv.write_wav(output_audio_path)

def resize_image_sstv(sstv_type,img,file_name):
    s_image = Image.open(img)
    w,h = s_image.size
    width,height=320,256

    scale_n = max(width/w,height/h)
    new_size=(int(w*scale_n),int(h*scale_n))
    image_resize = s_image.resize(new_size)

    image = Image.new("RGB",(width,height),(0,0,0))
    image_pos = ((width-new_size[0])//2,(height-new_size[1])//2)
    image.paste(image_resize,image_pos)
    #image = image.resize((160,256))
    encode_sstv(image, "./xunsi/sstv_temp_wav/"+file_name+".wav")

normal_sstv = on_command("锘 sstv测试", priority=10, block=True)
@normal_sstv.handle()
async def _(event: Event, arg: Message = CommandArg()):
    images = [d.data["url"] for d in event.get_message() if d.type =="image"]
    if images ==[]:
        await normal_sstv.finish("未包含图片信息")
    response = requests.get(images[0])
    image_data = BytesIO(response.content)
    time_str = time.strftime("%Y%m%d%H%M%S", time.localtime())
    resize_image_sstv("",image_data,time_str)
    # await normal_sstv.finish("生成成功")
    await normal_sstv.send(MessageSegment.record("file:///C:\\Users\\Administrator\\shiinano\\xunsi\\sstv_temp_wav\\"+time_str+".wav"))
    # await normal_sstv.finish(MessageSegment.at(event.get_user_id())
    #     + MessageSegment.image(images[0]))
