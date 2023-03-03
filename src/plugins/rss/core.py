from dateutil import parser
from pytz import timezone
from io import BytesIO
from datetime import datetime

import feedparser

from nonebot.adapters.onebot.v11.message import MessageSegment
from bs4 import BeautifulSoup
from src.utils.crawler.crawler import Crawler
from src.plugins.rss.config import RSS_CONF

TIMEZONE_SHANGHAI = timezone('Asia/Shanghai')
CRAWLER = Crawler()
OUTER_RSS_SERVER = 'https://rsshub.rssforever.com'
INNER_RSS_SERVER = 'https://rss.injahow.cn'

class RssSub():
  def __init__(self, url: str, id, need_proxy):
    if url.startswith('http://') or url.startswith('https://'):
      self.url = url
    elif need_proxy:
      self.url = OUTER_RSS_SERVER + url 
    else:
      self.url = INNER_RSS_SERVER + url 
    self.id = id
    self.updated = 0
    self.summary_processor = RssSub._default_summary_processor
    self.meta = {}
    self.post_des = []
    self.interval = 1200000 # milliseconds
    self.max_retrieve = 10
    self.silent = True

  @classmethod
  def _get_publish_ms(cls, entry):
    timestamp =  parser.parse(entry.published).timestamp()
    return round(timestamp * 1000)

  @classmethod
  def _default_summary_processor(cls, summary):
    soup = BeautifulSoup(summary, 'lxml')
    return (' '.join(soup.text.strip().split()))[:150] + '...'

  def _assemble_info(self, entry):
    headline = '消息来源未知'
    if self.meta:
      headline = '来自 “{}" 的新消息'.format(self.meta.get('title', 'Unknown'))
    
    title = entry.title
    link = entry.link
    publish = parser.parse(entry.published).astimezone(TIMEZONE_SHANGHAI)
    summary = self.summary_processor(entry.summary)

    soup = BeautifulSoup(entry.summary, 'lxml')
    img = soup.find('img')
    if img:
      img = CRAWLER.enable_proxy().get(img['src'])
      img = BytesIO(img.content)
    
    head = MessageSegment.text('{headline}\n{title}'.format(headline = headline, title = title))
    img = MessageSegment.image(img) if img else None
    content = MessageSegment.text('\n概览: {} \n发布于: {} \n链接: {}'.format(summary, publish, link))

    result = head + img + content if img else head + content
    return result

  def _parse_rss(self):
    rss = feedparser.parse(self.url, agent = RSS_CONF['user-agent'])
    if rss.status != 200:
      raise RuntimeError('parse {} failed, with status = {}'.format(self.url, rss.status))
    return rss.feed, rss.entries
  
  def _extract_new_entries(self, entries):
    return [entry for entry in entries if RssSub._get_publish_ms(entry) > self.updated]
  
  def add_dest(self, type, id):
    self.post_des.append({'type': type, 'id': id})
    return self
  
  def set_interval(self, interval = 0, milli = 1800000):
    if interval:
      self.interval = interval
    else:
      self.interval = milli
    return self
  
  def set_updated(self, updated):
    self.updated = updated
    return self

  def get_updated(self):
    return self.updated
  
  def get_interval(self):
    return self.interval
  
  def get_post_des(self):
    return self.post_des

  def set_max_retrieve(self, retrieve):
    self.max_retrieve = retrieve
    return self

  def set_silent(self, silent):
    self.silent = silent
  
  def retrieve(self):
    meta, entries = self._parse_rss()
    
    if not self.meta:
      self.meta = meta

    new_entries = self._extract_new_entries(entries)[:self.max_retrieve]
    results = [self._assemble_info(item) for item in new_entries]
    if self.updated == 0:
      results = results[:1]

    self.updated = round(datetime.now().timestamp() * 1000)
    return results