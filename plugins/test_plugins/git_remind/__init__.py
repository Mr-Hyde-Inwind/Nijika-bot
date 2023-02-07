import requests
import time
import datetime
from utils.json import json_parser
from nonebot import require
from nonebot import get_bot
from nonebot.adapters.onebot.v11 import Message

require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler
from apscheduler import events

content = ''
latest_id = -1
base_url = 'https://github.com/HibiKier/zhenxun_bot/'
api_url = 'https://api.github.com/networks/HibiKier/zhenxun_bot/events?per_page=100'
headers = {
  "Accept": "application/vnd.github+json",
  "X-GitHub-Api-Version": "2022-11-28"
}

_pattern = '''ビビ～　新しいイベントが発見しました
----------------------------------
[{event}]
提交数: {commit_cnt}
分支: {branch}
发布人: {user}
发布时间: {datetime}
commit link: {link}
repo link: https://github.com/HibiKier/zhenxun_bot
'''

async def say():
  global content
  try:
    response = requests.get(api_url, headers=headers)
    content = response.content.decode('utf-8')
  except Exception as err:
    pass
  else:
    await finish()

def pack_msg(parsed: dict):
  res = {}
  res['event'] = parsed['type']
  res['commit_cnt'] = parsed['payload']['size']
  res['branch'] = parsed['payload']['ref'].split('/')[-1]
  res['user'] = parsed['actor']['login']
  res['link'] = base_url + 'commit/' + parsed['payload']['head']

  date = datetime.datetime.fromisoformat(parsed['created_at'][:-1] + "+00:00").astimezone()
  res['datetime'] = date.strftime("%Y-%m-%d %H:%M:%S")

  return _pattern.format(**res)

async def finish():
  global latest_id
  bot = get_bot()
  if content:
    parsed = json_parser.parse(content)
    filted = list(filter(lambda x: x['type'] == 'PushEvent' or x['type'] == 'CreateEvent', parsed))
    if latest_id == -1:
      ans_str = '真寻 bot 监控组件首次启动, 监测到 %s 条更新\n接下来展示最新更新消息, 如果有的话 (笑' % len(filted)
      await bot.call_api("send_msg",
                         message_type='private',
                         user_id='2764143885',
                         message = Message(ans_str)) 
      time.sleep(2)
      if filted:
        ans_str = pack_msg(filted[0])
        await bot.call_api("send_msg",
                           message_type='private',
                           user_id='2764143885',
                           message = Message(ans_str)) 
    else:
      for item in filted:
        if item['id'] <= latest_id:
          break
        await bot.call_api("send_msg",
                           message_type='private',
                           user_id='2764143885',
                           message = Message(pack_msg(item))) 
    latest_id = parsed[0]['id']
  else:
    pass



scheduler.add_job(say, "interval",
                  minutes = 5,
                  next_run_time = datetime.datetime.now() + datetime.timedelta(seconds=5),
                  id='say_hello')
# scheduler.add_listener(finish, events.EVENT_JOB_EXECUTED)

