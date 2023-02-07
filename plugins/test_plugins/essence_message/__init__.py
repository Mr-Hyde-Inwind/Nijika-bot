from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Message
import json

matcher = on_command("essence", rule=to_me())

id = 901413269

@matcher.handle()
async def _(bot: Bot):
  # result = await bot.call_api("get_essence_msg_list", group_id = 901413269)
  result = await bot.call_api("get_msg", message_id=1688364533)
  #result = await bot.call_api("get_group_msg_history", group_id = 901413269)
  print(result)
  await matcher.finish(Message(result['message']))
