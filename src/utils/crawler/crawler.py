import tomli
import copy
import requests
from src.utils.configurator.configurator import GLOBAL_CONF
from pathlib import Path


CONFIG = Path(__file__).parent / 'crawler_conf.toml'

DEFAULT_CONF = {}

with open(CONFIG, 'rb') as f:
  DEFAULT_CONF = tomli.load(f)

class Crawler():
  __default_header = DEFAULT_CONF.get('headers', {})
  __default_proxies = {
    'http': GLOBAL_CONF['proxy'],
    'https': GLOBAL_CONF['proxy'],
  }

  def __init__(self, enable_proxy = False):
    self.use_proxy = enable_proxy

  def enable_proxy(self):
    self.use_proxy = True
    return self

  def disable_proxy(self):
    self.use_proxy = False
    return self

  def get_default_header(self):
    return copy.deepcopy(type(self).__default_header)

  def get(self, url, headers = __default_header, params = {}, data = {}, proxies = __default_proxies):
    if self.use_proxy:
      return requests.get(url, headers = headers, params = params, data =data, proxies = proxies)
    else:
      return requests.get(url, headers = headers, params = params, data =data, proxies = {})

  def post(self, url, headers = __default_header, params = {}, data = {}, proxies = __default_proxies):
    if self.use_proxy:
      return requests.post(url, headers = headers, params = params, data =data, proxies = proxies)
    else:
      return requests.post(url, headers = headers, params = params, data =data, proxies = {})


if __name__ == '__main__':
  pass