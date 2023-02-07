from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.rule import (
  to_me
)
from nonebot.params import ArgPlainText, Arg, CommandArg

web_list = dict()

web_list['bilibili'] = 'https://www.bilibili.com'
web_list['原神规划'] = 'https://seelie.me/planner'
web_list['nonebot文档'] = 'https://v2.nonebot.dev/docs'
web_list['onebot文档'] = 'https://onebot.adapters.nonebot.dev'

bookmarks = on_command("bm", aliases = {"书签"})

@bookmarks.handle()
async def _(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()
    if plain_text:
      matcher.set_arg("label", args)

@bookmarks.got("label", prompt = "想要获取的网页标签是? \"list\" 获取列表")
async def _(label: Message = Arg(), label_str: str = ArgPlainText("label")):
  if label_str == 'list':
    await bookmarks.finish('\n'.join(item for item in web_list.keys()))
  if label_str not in web_list.keys():
    await bookmarks.finish("这样的网站找不到辣")
  else:
    await bookmarks.finish(web_list[label_str]) 