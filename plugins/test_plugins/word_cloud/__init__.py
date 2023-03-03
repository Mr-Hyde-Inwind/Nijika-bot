import re
import PIL
import numpy as np
import jieba.analyse
import base64
from io import BytesIO
from wordcloud import WordCloud
from utils.config import path_config
from nonebot import require
from datetime import datetime, timedelta
from utils.db import db_manager
require("nonebot_plugin_apscheduler")

from nonebot_plugin_apscheduler import scheduler
from nonebot import get_bot
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot import on_command
from nonebot.rule import to_me

# 测试用群
TEST_GROUP = 901413269

SQL = '''
SELECT PLAIN FROM CHAT_HISTORY
WHERE
  PLAIN NOT NULL
  AND PLAIN != ""
  AND GROUP_ID = :group_id
  AND TIMESTAMP BETWEEN :start AND :end
'''

BACKGROUND = path_config.IMAGE_PATH / 'word_cloud' / 'nijika.png'
FONT = path_config.FONT_PATH / 'msyh.ttf'

def get_chat_history(gid, start, end):
  conn = db_manager.get_default_connection()
  params = {
    'group_id': gid,
    'start': start,
    'end': end
  }
  return conn.query(SQL, params = params)

def preprocess(textList):
  text = " ".join(item[0] for item in textList)
  return re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", text)

def build_word_cloud(textList):
  wordsWithWeight = jieba.analyse.extract_tags(preprocess(textList),
                                                topK = min(len(textList), 20000),
                                                withWeight = True, allowPOS = ())
  words = []
  weight = []
  for item in wordsWithWeight:
    words.append(item[0])
    weight.append(item[1])

  im = PIL.Image.open(BACKGROUND.absolute().as_posix())
  wc = WordCloud(font_path = FONT.absolute().as_posix(),
                 width = 1920,
                 height = 1080,
                 background_color = 'white',
                 mask = np.array(im))
  wc.generate_from_frequencies(dict(zip(words, weight)))
  buf = BytesIO()
  img = wc.to_image()
  img.save(buf, format = "PNG")
  return base64.b64encode(buf.getvalue()).decode()


job_defaults = {
  'coalesce': True,
  'max_instance': 2,
  'misfire_grace_time': 300000
}

scheduler.configure(job_defaults = job_defaults)

@scheduler.scheduled_job("cron", hour="7")
async def post_word_cloud():
  end = datetime.now()
  start = end - timedelta(hours = 24)

  textList = get_chat_history(TEST_GROUP, int(start.timestamp()), int(end.timestamp()))
  img_base64 = build_word_cloud(textList)   

  msg = MessageSegment.text("昨日的群吹逼印象是") + MessageSegment.image("base64://" + img_base64)

  _ = await get_bot().send_group_msg(group_id = TEST_GROUP, message = msg)


# test = on_command("test_word_cloud", rule = to_me(), priority = 5, block = True)
# 
# @scheduler.scheduled_job("interval", minutes = 10, id = 'test_word_cloud')
# async def _():
#   end = datetime.now()
#   start = end - timedelta(hours = 24)
# 
#   textList = get_chat_history(TEST_GROUP, int(start.timestamp()), int(end.timestamp()))
#   img_base64 = build_word_cloud(textList)   
# 
#   msg = MessageSegment.text("昨日的群吹逼印象是") + MessageSegment.image("base64://" + img_base64)
# 
#   _ = await get_bot().send_private_msg(user_id = 2764143885, message = msg)
