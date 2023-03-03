import sys
import asyncio
import httpx
from pathlib import Path

############################## TEST ######################################
if __name__ == '__main__':
  root = Path(__file__).absolute().parents[3]
  sys.path.append(root.as_posix())

import src.utils.crawler.config as config


HEADERS = 'headers'
PARAMS = 'params'
DATA = 'data'
PROXY = 'proxy'
URL = 'url'
TIMEOUT = 'timeout'

class AsyncCrawler():
  def __init__(self):
    self.default_headers = config.get_default_conf()[HEADERS]
    self.use_proxy = False

    proxy = config.get_default_conf()[PROXY]
    proxies = {
      'http://': proxy,
      'https://': proxy,
    }
    self.default_proxy = proxies
    self.default_timeout = 20

    # init context
    self._done_after_task()

  def _done_after_task(self):
    self.context = {
      PARAMS: {},
      DATA: {},
      URL: ''
    }

  async def get(self):
    headers = self.context.get(HEADERS, self.default_headers)
    params = self.context.get(PARAMS, {})
    url = self.context[URL]
    timeout = self.context.get(TIMEOUT, self.default_timeout)

    if self.use_proxy:
      proxies = self.context[PROXY] if PROXY in self.context.keys() else self.default_proxy
    else:
      proxies = None

    async with httpx.AsyncClient(proxies = proxies) as client:
      return await client.get(url = url,
                             params = params,
                             headers = headers,
                             timeout = timeout)

  async def post(self):
    pass

  def get_default_headers(self):
    return self.default_headers

  def enable_proxy(self):
    self.use_proxy = True
    return self

  def disable_proxy(self):
    self.use_proxy = False
    return self

  def with_headers(self, headers: dict):
    self.context[HEADERS] = headers
    return self

  def with_params(self, params: dict):
    self.context[PARAMS] = params
    return self

  def with_data(self, data: dict):
    self.context[DATA] = data
    return self
  
  def with_timeout(self, timeout):
    self.context[TIMEOUT] = timeout
    return self

  def with_proxy(self, proxy: str):
    proxies = {
      'http://': proxy,
      'https://': proxy,
    }
    self.context[PROXY] = proxies
    return self

  def with_url(self, url: str):
    self.context[URL] = url
    return self

if __name__ == '__main__':
  crawler = AsyncCrawler()
  headers = crawler.get_default_headers()
  headers['referer'] = 'https://store.steampowered.com/specials'
  params = {
    'cc': 'cn',
    'l': 'schinese',
    'flavor': 'contenthub_all',
    'start': 0,
    'count': 10,
    'return_capsules': 'true',
    'origin': 'https://store.steampowered.com',
    'strContentHubType': 'specials',
  }

  crawl = (crawler.with_headers(headers)
                 .with_params(params)
                 .with_url(url = 'https://store.steampowered.com/saleaction/ajaxgetsaledynamicappquery')
                 .enable_proxy()
  )

  async def wrap():
    response = await crawl.get()
    print(response)
    return response.text

  loop = asyncio.get_event_loop()
  task = loop.create_task(wrap())
  loop.run_until_complete(task)
  print(task.result())
