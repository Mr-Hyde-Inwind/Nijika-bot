import feedparser
from bs4 import BeautifulSoup
from src.utils.crawler.async_crawler import AsyncCrawler
from src.plugins.rss.config import RSS_CONF
from io import BytesIO
from pytz import timezone
from datetime import datetime, timedelta
from dateutil import parser

from nonebot import require
require('nonebot_plugin_apscheduler')
from nonebot_plugin_apscheduler import scheduler

from nonebot import get_bot
from nonebot.adapters.onebot.v11.message import MessageSegment

from src.plugins.rss.core import RssSub

CRAWLER = AsyncCrawler()
RSS_SUB = '/bbc/world'
SHANGHAI = timezone('Asia/Shanghai')
LAST_TIMESTAMP = 0

def get_rss_url():
  return RSS_CONF['rsshub'] + RSS_SUB

def get_entries():
  return feedparser.parse(get_rss_url(), agent = RSS_CONF['user-agent']).entries

async def extract_info(entry):
  title = entry.title
  link = entry.link
  publish = parser.parse(entry.published).astimezone(SHANGHAI)

  soup = BeautifulSoup(entry.summary, 'lxml')
  summary = soup.text[:300] + '...'

  img = soup.find('img').get('src', None)
  if img:
    img = await CRAWLER.with_url(img).enable_proxy().get()
    img = BytesIO(img.content)
  
  return {
    'title': title,
    'date': str(publish),
    'img': img,
    'summary': summary,
    'link': link,
  }

def get_publish_date(entry):
  timestamp =  parser.parse(entry.published).timestamp()
  return round(timestamp)

async def post(post_type, user_id, entry):
  bot = get_bot()
  info = await extract_info(entry)
  text = '标题: {} \n概览: {} \n发布于: {} \nlink: {}'.format(info.get('title'),
                                                             info.get('summary'),
                                                             info.get('date'),
                                                             info.get('link'))
  msg = MessageSegment.text(text)
  if info.get('img'):
    msg = MessageSegment.image(info.get('img')) + msg

  if post_type == 'p':
    await bot.send_private_msg(user_id = user_id, message = msg)
  if post_type =='g':
    await bot.send_group_msg(group_id = user_id, message = msg)

async def init():
  global LAST_TIMESTAMP
  bot = get_bot()
  msg = MessageSegment.text('首次运行 bbc 新闻订阅, 将展示最新一条咨询')
  await bot.send_private_msg(user_id = 2764143885, message = msg)
  
  entries = get_entries()
  if len(entries) > 0:
    await post('p', 2764143885, entries[0])
    LAST_TIMESTAMP = get_publish_date(entries[0])
  else:
    msg = MessageSegment.text('当前没有从 RSS 订阅 {} 中获取到信息, 将过后重试... 或者请管理员检查日志排查问题.')
    bot.send_private_msg(user_id = 2764143885, message = msg)

async def job():
  global LAST_TIMESTAMP
  print('current timestamp: ', LAST_TIMESTAMP)
  if LAST_TIMESTAMP == 0:
    await init()
  else:
    timestamp = 0
    entries = get_entries()
    print('0\'s title: ', entries[0].title)
    new_entries = [entry for entry in entries if get_publish_date(entry) > LAST_TIMESTAMP]
    for entry in new_entries:
      await post('p', 2764143885, entry)
      timestamp = max(LAST_TIMESTAMP, get_publish_date(entry))
    LAST_TIMESTAMP = max(LAST_TIMESTAMP, timestamp)

# @scheduler.scheduled_job('interval', minutes = 30, id = 'bbc', next_run_time = datetime.now() + timedelta(seconds=10))
# async def _():
#   await job()

# bbc = RssSub(get_rss_url(), 'bbc-world')
# (bbc.add_dest('p', 2764143885)
#     # .add_dest('g', 901413269)
#     .set_interval(60)
#     .start())