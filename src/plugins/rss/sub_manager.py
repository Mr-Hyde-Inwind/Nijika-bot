import random
from datetime import datetime, timedelta
from queue import LifoQueue, Empty

from src.plugins.rss.config import RSS_CONF
from src.plugins.rss.core import RssSub
from nonebot import get_bot
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot import require
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

class SubManager():

  def __init__(self):
    self.posted = 0
    self.msg_need_post = LifoQueue(1000)
    self.subs = []

  def _load_from_dict(self, entry):
    sub = RssSub(url = entry['url'], id = entry['id'], need_proxy = entry['need_proxy'])
    sub.set_max_retrieve(entry.get('max_retrieve', 10))
    sub.set_interval(entry.get('refresh_interval', 1800000))
    sub.set_silent(entry.get('silent', True))
    for dest in entry['dest']:
      sub.add_dest(type = dest['type'], id = dest['id'])
    self.subs.append(sub) 


  def _load_all_from_conf(self):
    for entry in RSS_CONF['subscribe']:
      self._load_from_dict(entry)

  def _should_retrieve(self, sub: RssSub):
    # 启动时打散任务
    if sub.get_updated() == 0:
      return random.random() < 1/2
    next_retrieve_time = sub.get_updated() + sub.get_interval()
    return round(datetime.now().timestamp() * 1000) >= next_retrieve_time
  
  async def _retrieve(self):
    available_subs = [sub for sub in self.subs if self._should_retrieve(sub)]
    for sub in available_subs:
      first_retrieve = sub.updated == 0
      try:
        msgs = sub.retrieve()
      except Exception as e:
        err = MessageSegment.text('获取订阅 {} 失败 with err = {}'.format(sub.id, str(e)))
        self.msg_need_post.put_nowait({'sub': sub, 'msg': err})
      else:
        if first_retrieve and sub.silent:
          continue
        for msg in msgs:
          self.msg_need_post.put_nowait({'sub': sub, 'msg': msg})

  async def _post(self):
    bot = get_bot()
    try:
      packet = self.msg_need_post.get_nowait()
    except Exception as e:
      if not isinstance(e, Empty):
        print(e)
    else:
      post_dests = packet['sub'].get_post_des()
      for des in post_dests:
        if des['type'] == 'p':
          await bot.send_private_msg(user_id = des['id'], message = packet['msg'])
        if des['type'] == 'g':
          await bot.send_group_msg(group_id = des['id'], message = packet['msg'])

  def start(self):
    self._load_all_from_conf()
    scheduler.add_job(self._retrieve, 'interval', seconds = 300, next_run_time = datetime.now() + timedelta(seconds = 15))
    scheduler.add_job(self._post, 'interval', seconds = 30)
    
MANAGER = SubManager()
MANAGER.start()

def get_manager():
  return MANAGER