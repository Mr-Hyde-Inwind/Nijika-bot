'''
# Description
当前为用于简单记录 TODO 的插件
使用 sqlite 进行记录

# 数据库

## 数据库信息
database: ryou.db
table: todo

## 数据库表设计
- ID            
- QQ_ID        QQ 号                                   TEXT      不可为空
- timestamp    该 todo 创建时间的时间戳, 由系统自动创建   TEXT      不可为空
- content      记录 todo 内容                           TEXT      不可为空

# 使用限制
- 目前每个用户都可以接入该功能
- 每个 ID 下最多有 20 条记录

# 机器人控制命令

'''

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.permission import SUPERUSER
from nonebot.params import ArgPlainText, CommandArg
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from utils.db import db_manager

todo = on_command("todo", rule = to_me(), permission = SUPERUSER)


LIST_COMMAND = ['list']
HELP_COMMAND = ['help']

_EMPTY_LIST = '清单空空如也, 开摆!'
_NEED_PARAMS = '请指定功能和必要参数捏, 或者试试 todo help 来获取帮助吧'
_HELP_MSG = '''
todo [ACTTION] [TODO/EVENT ID]
Avaliable action:
  list:   list all todo events associated with your ID.
  add:    Add a new event to your list.
  finish: Mark a event finished in your list and delete it.
'''






@todo.handle()
async def _(args: Message = CommandArg()):
  plain_args = args.extract_plain_text().split()
  if len(plain_args) < 1: 
    await todo.finish(_NEED_PARAMS)
  elif len(plain_args) == 1:
    if plain_args[0].lower() in LIST_COMMAND:
      await todo.finish(_EMPTY_LIST)
    elif plain_args[0].lower() in HELP_COMMAND:
      await todo.finish(_HELP_MSG)
  elif len(plain_args) >= 2:
    await todo.sned("")
