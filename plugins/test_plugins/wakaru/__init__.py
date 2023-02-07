from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.message import MessageSegment
from utils.config.path_config import AUDIO_PATH

OMOSHIROI = AUDIO_PATH / 'nijika' / 'omoshiroi.mp3'

womoshiroi = on_command("omoshiroi", aliases = {'救世啊', '就是啊', '就是'}, priority = 5, block =  True)

@womoshiroi.handle()
async def _():
  print(OMOSHIROI.absolute())
  if OMOSHIROI.exists():
    print('file exist')
  else:
    print('file do not exist')
  await womoshiroi.finish(MessageSegment.record(OMOSHIROI))