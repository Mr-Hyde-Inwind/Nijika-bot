from typing import Union
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, GroupMessageEvent
from nonebot.permission import SUPERUSER
from src.plugins.rss.sub_manager import MANAGER


summary = on_command('sub_summary', priority = 5, rule = to_me(), block = True, permission = SUPERUSER)

@summary.handle()
async def _(event: Union[PrivateMessageEvent, GroupMessageEvent]):
  reports = []
  reports.append('ID   last_updated   next_update')
  for sub in MANAGER.subs:
    report = '{id}  {updated}  {next_update}'.format(id = sub.id, updated = sub.updated, next_update = sub.updated + sub.interval)
    reports.append(report)
  reports.append('当前队列中有 {} 条新消息等待输出'.format(MANAGER.msg_need_post.qsize()))

  await summary.send('\n'.join(reports))
