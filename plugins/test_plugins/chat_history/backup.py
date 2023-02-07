from nonebot import on_message
from nonebot.adapters.onebot.v11 import Event, MessageEvent, GroupMessageEvent
from utils.db import db_manager
from nonebot.rule import to_me
from nonebot import get_bot
import copy

def rule(event: Event) -> bool:
  return isinstance(event, MessageEvent)

sql = '''
INSERT INTO CHAT_HISTORY (USR_ID, GROUP_ID, MSG, PLAIN, TIMESTAMP)
VALUES (:user_id, :group_id, :msg, :plain, :timestamp)
'''

message_backup = on_message(rule = rule, priority = 1, block = False)

async def backup_msg(msg_dict):
  try:
    db_manager.get_default_connection().execute(sql, msg_dict)
  except Exception as e:
    print(e)
    print("备份消息失败" + msg_dict['msg'])
  else:
    print("成功备份: " + msg_dict['msg'])


@message_backup.handle()
async def _(event: MessageEvent):
  if not event.raw_message:
    return
  params = {'user_id': event.user_id,
    'group_id': None,
    'msg': event.raw_message,
    'plain': event.message.extract_plain_text(),
    'timestamp': event.time
  }
  if isinstance(event, GroupMessageEvent):
    params['group_id'] = event.group_id
  await backup_msg(copy.deepcopy(params))
