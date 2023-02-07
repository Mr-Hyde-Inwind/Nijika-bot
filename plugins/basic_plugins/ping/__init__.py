from nonebot import on_command
from nonebot.rule import to_me


ping = on_command("ping", rule=to_me(), priority=5)

@ping.handle()
async def pang():
  await ping.finish("はいはい、ここにいるよ～")
