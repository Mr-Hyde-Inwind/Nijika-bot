import sqlite3
import matplotlib.pyplot as plt
import jieba.analyse
import numpy as np
from wordcloud import WordCloud
import PIL
import re

SQL = '''
SELECT PLAIN
FROM CHAT_HISTORY
WHERE
  GROUP_ID = 901413269
  AND PLAIN NOT NULL
  AND PLAIN != ""
  AND TIMESTAMP BETWEEN CAST(strftime('%s', 'now') as INTEGER) - 3600*24 AND CAST(strftime('%s', 'now') as INTEGER)
'''

SQL = '''
SELECT PLAIN
FROM CHAT_HISTORY
WHERE
  GROUP_ID = 901413269
  AND PLAIN NOT NULL
  AND PLAIN != ""
'''


# def pre_process(text):
#   text = re.sub(r"https?://[\w/:%#\$&\?\(\)~\.=\+\-]+", "", text)
#   return text
# 
# with sqlite3.connect('ryou.db') as conn:
#   res = conn.execute(SQL)
#   lst = res.fetchall()
#   text = " ".join([item[0] for item in lst])
#   res = jieba.analyse.extract_tags(pre_process(text), topK = 20, withWeight = True, allowPOS = ())
#   print(res)
  

with open('/home/suzuhara/workPlace/Practice/python/crawler/tags', 'rt', encoding = 'utf-8') as f:
  text = " ".join(f.readlines())
  res = jieba.analyse.extract_tags(text, topK = min(10000, len(text.split())), withWeight = True, allowPOS = ())
    
  name = []
  value = []
  for item in res:
    name.append(item[0])
    value.append(item[1])
  
  im = PIL.Image.open('nijika.png')
  
  wc = WordCloud(font_path = '/home/suzuhara/workPlace/Project/Nijika-bot/resources/font/msyh.ttf',
                 width = 1000,
                 height = 700,
                 background_color = 'white',
                 mask = np.array(im),
                 scale = 20)
  wc.generate_from_frequencies(dict(zip(name, value)))
  wc.to_file('test.png')




